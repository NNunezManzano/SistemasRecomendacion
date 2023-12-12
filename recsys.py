import pandas as pd
import numpy as np

import sys
import json

import lightfm as lfm
from lightfm import data
from lightfm import cross_validation
from lightfm import evaluation

import os 

from data.data_src import Data_source

dsrc = Data_source('Videojuegos.db')

def crear_usuario(id_usuario):    
    query = "INSERT INTO usuarios(id_usuario) VALUES (?) ON CONFLICT DO NOTHING;" 
    dsrc.sql_execute(query, (id_usuario,))
    return

def insertar_review(id_juego, id_usuario, rating, interacciones="reviews"):
    query = f"INSERT INTO {interacciones}(id_review, id_juego, id_usuario, rating) VALUES (?, ?, ?, ?)" #ON CONFLICT (id_review) DO UPDATE SET rating=?;"" # si el rating existia lo actualizo
    dsrc.sql_execute(query, (id_juego+id_usuario,id_juego, id_usuario, rating))
    return

def valorados(id_usuario, interacciones="reviews"):
    query = f"SELECT * FROM {interacciones} WHERE id_usuario = ? AND rating > 0"
    valorados = dsrc.sql_select(query, (id_usuario,))
    return valorados

def ignorados(id_usuario, interacciones="reviews"):
    query = f"SELECT * FROM {interacciones} WHERE id_usuario = ? AND rating = 0"
    ignorados = dsrc.sql_select(query, (id_usuario,))
    return ignorados

def datos_juegos(id_juego):
    query = f"SELECT DISTINCT * FROM juegos WHERE id_juego IN ({','.join(['?']*len(id_juego))})"
    libros = dsrc.sql_select(query, id_juego)
    return libros

def reset_usuario(id_usuario, interacciones="reviews"):
    query = f"DELETE FROM {interacciones} WHERE id_usuario = ?;"
    dsrc.sql_execute(query, (id_usuario,))
    return

def recomendar_top_9(id_usuario, interacciones="reviews"):
    query = f"""
        SELECT id_juego, AVG(rating) as rating, count(*) AS cant
          FROM {interacciones}
         WHERE id_juego NOT IN (SELECT id_juego FROM {interacciones} WHERE id_usuario = ?)
           AND rating > 0
         GROUP BY 1
         ORDER BY 3 DESC, 2 DESC
         LIMIT 9
    """
    id_juego = [r["id_juego"] for r in dsrc.sql_select(query, (id_usuario,))]
    return id_juego

def recomendar_lightfm(id_usuario, interacciones="reviews"):
    # TODO: optimizar hiperparámetros
    # TODO: entrenar el modelo de forma parcial
    # TODO: user item_features y user_features
    # TODO: usar los items ignorados (usar pesos)

    con = dsrc.create_connection('Videojuegos.db')

    df_reviews = pd.read_sql_query(f"SELECT * FROM {interacciones} WHERE rating > 0", con)
    df_details = pd.read_sql_query("SELECT * FROM juegos", con)
    con.close()

   # Inicilizo el dataset de lightfm
    ds = lfm.data.Dataset()
    ds.fit(users=df_reviews["id_usuario"].unique(), items=df_reviews["id_juego"].unique())
    
    user_id_map, user_feature_map, item_id_map, item_feature_map = ds.mapping()
    (interactions, weights) = ds.build_interactions(df_reviews[["id_usuario", "id_juego", "rating"]].itertuples(index=False))

    model = lfm.LightFM(no_components=20, k=5, n=10, learning_schedule='adagrad', loss='logistic', learning_rate=0.05, rho=0.95, epsilon=1e-06, item_alpha=0.0, user_alpha=0.0, max_sampled=10, random_state=42)
    model.fit(interactions, sample_weight=weights, epochs=10)

    juegos_jugados = df_reviews.loc[df_reviews["id_usuario"] == id_usuario, "id_juego"].tolist()
    todos_los_juegos = df_details["id_juego"].tolist()
    juegos_no_jugados = set(todos_los_juegos).difference(juegos_jugados)
    predicciones = model.predict(user_id_map[id_usuario], [item_id_map[l] for l in juegos_no_jugados])

    recomendaciones = sorted([(p, l) for (p, l) in zip(predicciones, juegos_no_jugados)], reverse=True)[:9]
    recomendaciones = [juego[1] for juego in recomendaciones]
    return recomendaciones

def recomendar(id_usuario, interacciones="reviews"):
    # TODO: combinar mejor los recomendadores
    # TODO: crear usuarios fans para llenar la matriz    

    cant_valorados = len(valorados(id_usuario, interacciones))

    if cant_valorados == 0:
        print("recomendador: top9", file=sys.stdout)
        id_juego = recomendar_top_9(id_usuario, interacciones)
    else:
        print("recomendador: lightfm", file=sys.stdout)
        id_juego = recomendar_lightfm(id_usuario, interacciones)


    # TODO: como completo las recomendaciones cuando vienen menos de 9?

    recomendaciones = datos_juegos(id_juego)   

    return recomendaciones




'''
Modelo Light FM solo con datos de interacciones
'''
#Obtengo los datos de la base de datos
conn = dsrc.create_connection('Videojuegos.db')
df_reviews = pd.read_sql_query(f"SELECT * FROM reviews", conn)

# Inicilizo el dataset de lightfm
ds = lfm.data.Dataset()
ds.fit(users=df_reviews["id_usuario"].unique(), items=df_reviews["id_juego"].unique())

#Mapeo interacciones y pesos
#user_id_map, user_feature_map, item_id_map, item_feature_map = ds.mapping()
(interactions, weights) = ds.build_interactions(df_reviews[["id_usuario", "id_juego", "rating"]].itertuples(index=False))

#Creo un sample de train y test
(train, test) = lfm.cross_validation.random_train_test_split(interactions, test_percentage=0.2, random_state=110293)
(train_w, test_w) = lfm.cross_validation.random_train_test_split(weights, test_percentage=0.2, random_state=110293)

#Creo el modelo
model = lfm.LightFM(no_components=10, k=3, n=20, learning_schedule='adagrad', loss='logistic', learning_rate=0.05, rho=0.95, epsilon=1e-06, item_alpha=0.0, user_alpha=0.0, max_sampled=10, random_state=110293)
model.fit_partial(train, sample_weight=train_w, epochs=10)

print(f'Resultado de testing para el modelo 1: {lfm.evaluation.precision_at_k(model, test,k=3, num_threads=2).mean()}')

'''
Modelo Light FM con datos de cada juego
'''
#Obtengo datos de los juegos
df_details = pd.read_sql_query(f"SELECT * FROM juegos", conn)

#Inicializo el modelo
ds_details = lfm.data.Dataset()

#Genero una lista con los features de cada juego
game_features= df_details['Rating'].explode().unique().tolist() + df_details.Distribuidor.explode().unique().tolist() + df_details.Genero.explode().unique().tolist()

#Genero el modelo y asigno los features
ds_details.fit(users=df_reviews["id_usuario"].unique(), items=df_reviews["id_juego"].unique(), item_features=game_features)

#Elimino 
juegos_con_reviews=df_reviews["id_juego"].unique()

df_details["to_drop"] = df_details.id_juego.apply(lambda x: 0 if x in juegos_con_reviews else 1)    

df_details.drop(df_details[df_details.to_drop == 1].index, inplace = True)
df_details.drop(columns='to_drop', inplace = True)

game_features_ls = []

for index, row in df_details.iterrows():
  
  if type(row.Genero) == list:
    genero = str(row.Genero[0])
    game_features_ls.append((row.id_juego, (row.Rating, row.Distribuidor, genero)))
  else :
    game_features_ls.append((row.id_juego, (row.Rating, row.Distribuidor, row.Genero)))
  
for features in game_features_ls:
  if type(features[0]) == list:
    print(features)
  for feature in features[1]:
    if type(feature) == list:
      print(features)

game_features_build = ds_details.build_item_features(game_features_ls)

#user_id_map, user_feature_map, item_id_map, item_feature_map = ds.mapping()
(interactions_dl, weights_dl) = ds_details.build_interactions(df_reviews[["id_usuario", "id_juego", "rating"]].itertuples(index=False))

(train_dl, test_dl) = lfm.cross_validation.random_train_test_split(interactions_dl, test_percentage=0.2, random_state=110293)
(train_w_dl, test_w_dl) = lfm.cross_validation.random_train_test_split(weights_dl, test_percentage=0.2, random_state=110293)

#model_dl = lfm.LightFM(no_components=10, k=5, n=20, learning_schedule='adagrad', loss='logistic', learning_rate=0.05, rho=0.95, epsilon=1e-06, item_alpha=0.0, user_alpha=0.0, max_sampled=10, random_state=110293)
model_dl = lfm.LightFM(learning_rate=0.03, loss='logistic', no_components=25, random_state=110293)
#model_dl.fit(train_dl, sample_weight=train_w_dl, item_features=game_features_build, epochs=100)
model_dl.fit(train_dl, sample_weight=train_w_dl, item_features=game_features_build, epochs=100)

print(f'Resultado de testing para el modelo 2: {lfm.evaluation.precision_at_k(model, test_dl,k=5, num_threads=2).mean()}')