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
    positive = 1 if rating > 5 else 0
    query = f"INSERT INTO {interacciones}(id_review, id_juego, id_usuario, rating, Positive_rate) VALUES (?, ?, ?, ?, ?) ON CONFLICT (id_review) DO UPDATE SET rating=?, Positive_rate=?;" # si el rating existia lo actualizo
    dsrc.sql_execute(query, (id_juego+id_usuario,id_juego, id_usuario, rating, positive, rating, positive))
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
    juegos = dsrc.sql_select(query, id_juego)
    return juegos

def reset_usuario(id_usuario, interacciones="reviews"):
    query = f"DELETE FROM {interacciones} WHERE id_usuario = ?;"
    dsrc.sql_execute(query, (id_usuario,))
    return

def recomendar_top_9_por_genero(id_usuario, interacciones="reviews"):
    categoria = np.random.choice(["RPG","estrategia","shooter","sport","accion","carreras","Otros"],3)
    query = f"""
        SELECT * FROM (SELECT r.id_juego, AVG(r.rating) as rating, count(*) AS cant
                  FROM reviews r 
                  JOIN juegos j
                  	ON J.id_juego = r.id_juego
                 WHERE r.id_juego NOT IN (SELECT r2.id_juego FROM reviews r2  WHERE r2.id_usuario = ?)
                   AND r.rating > 0
                   AND j.Sub_genero = ?
                 GROUP BY 1
                 HAVING cant > 3
                 ORDER BY 2 DESC, 3 DESC         
                 LIMIT 3)
        UNION
        SELECT * FROM (SELECT r.id_juego, AVG(r.rating) as rating, count(*) AS cant
                  FROM reviews r 
                  JOIN juegos j
                  	ON J.id_juego = r.id_juego
                 WHERE r.id_juego NOT IN (SELECT r2.id_juego FROM reviews r2  WHERE r2.id_usuario = ?)
                   AND r.rating > 0
                   AND j.Sub_genero = ?
                 GROUP BY 1
                 HAVING cant > 3
                 ORDER BY 2 DESC, 3 DESC         
                 LIMIT 3)
        UNION
        SELECT * FROM (SELECT r.id_juego, AVG(r.rating) as rating, count(*) AS cant
                  FROM reviews r 
                  JOIN juegos j
                  	ON J.id_juego = r.id_juego
                 WHERE r.id_juego NOT IN (SELECT r2.id_juego FROM reviews r2  WHERE r2.id_usuario = ?)
                   AND r.rating > 0
                   AND j.Sub_genero = ?
                 GROUP BY 1
                 HAVING cant > 3
                 ORDER BY 2 DESC, 3 DESC         
                 LIMIT 3);   
         
    """
    id_juego = [r["id_juego"] for r in dsrc.sql_select(query, (id_usuario,categoria[0],id_usuario,categoria[1],id_usuario,categoria[2]))]
    return id_juego

def recomendar_top_9(id_usuario, interacciones="reviews"):
    query = f"""
        SELECT * FROM (SELECT r.id_juego, AVG(r.rating) as rating, count(*) AS cant
                  FROM reviews r 
                  JOIN juegos j
                  	ON J.id_juego = r.id_juego
                 WHERE r.id_juego NOT IN (SELECT r2.id_juego FROM reviews r2  WHERE r2.id_usuario = ?)
                   AND r.rating > 0
                 GROUP BY 1
                 HAVING cant > 3
                 ORDER BY 2 DESC, 3 DESC         
                 LIMIT 9);   
         
    """
    id_juego = [r["id_juego"] for r in dsrc.sql_select(query, (id_usuario,))]
    return id_juego

def recomendar_top_n(id_usuario, interacciones="reviews", n = 1):
    query = f"""
        SELECT * FROM (SELECT r.id_juego, AVG(r.rating) as rating, count(*) AS cant
                  FROM reviews r 
                  JOIN juegos j
                  	ON J.id_juego = r.id_juego
                 WHERE r.id_juego NOT IN (SELECT r2.id_juego FROM reviews r2  WHERE r2.id_usuario = ?)
                   AND r.rating > 0
                 GROUP BY 1
                 HAVING cant > ?
                 ORDER BY 2 DESC, 3 DESC         
                 LIMIT 9);   
         
    """
    id_juego = [r["id_juego"] for r in dsrc.sql_select(query, (id_usuario,n))]
    return id_juego

def recomendar_top_9_no_jugo_a_nada(id_usuario, interacciones="reviews"):
    query = f"""
        SELECT * FROM (SELECT r.id_juego, AVG(r.rating) as rating, count(*) AS cant
                  FROM reviews r 
                  JOIN juegos j
                  	ON J.id_juego = r.id_juego
                 WHERE r.id_juego NOT IN (SELECT r2.id_juego FROM reviews r2  WHERE r2.id_usuario = ?)                   
                 GROUP BY 1
                 ORDER BY 2 DESC, 3 DESC         
                 LIMIT 9);   
         
    """
    id_juego = [r["id_juego"] for r in dsrc.sql_select(query, (id_usuario,))]
    return id_juego

def recomendar_lightfm(id_usuario, interacciones="reviews", clicks=1):
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

    model = lfm.LightFM(no_components=1, k=1, n=1, learning_schedule='adagrad', loss='logistic', learning_rate=0.05, rho=0.95, epsilon=1e-06, item_alpha=0.0, user_alpha=0.1, random_state=110293)
    model.fit(interactions, sample_weight=weights, epochs=10)

    juegos_jugados = df_reviews.loc[df_reviews["id_usuario"] == id_usuario, "id_juego"].tolist()
    
    juegos_con_reviews=df_reviews["id_juego"].unique()
    df_details["to_drop"] = df_details.id_juego.apply(lambda x: 0 if x in juegos_con_reviews else 1)    
    df_details.drop(df_details[df_details.to_drop == 1].index, inplace = True)
    df_details.drop(columns='to_drop', inplace = True)

    con = dsrc.create_connection('Videojuegos.db')
    juegos_ignorados = pd.read_sql_query(f"SELECT * FROM {interacciones} WHERE id_usuario = '{id_usuario}'", con).id_juego.tolist()
    con.close()

    todos_los_juegos = df_details["id_juego"].tolist()
    juegos_no_jugados = set(todos_los_juegos).difference(juegos_jugados)
    if clicks % 4 != 0 :
      juegos_no_jugados = set(juegos_no_jugados).difference(juegos_ignorados)
    predicciones = model.predict(user_id_map[id_usuario], [item_id_map[l] for l in juegos_no_jugados])

    recomendaciones = sorted([(p, l) for (p, l) in zip(predicciones, juegos_no_jugados)], reverse=True)[:9]
    recomendaciones = [juego[1] for juego in recomendaciones]
    return recomendaciones

def recomendar(id_usuario, interacciones="reviews", clicks=1): 

    cant_valorados = len(valorados(id_usuario, interacciones))

    if cant_valorados < 3:
        print("recomendador: top_9_por_genero", file=sys.stdout)
        id_juego = recomendar_top_9_por_genero(id_usuario, interacciones)
        
        recomendaciones = datos_juegos(id_juego)
        
        if len(recomendaciones) < 9:
          print("recomendador: top_n", file=sys.stdout)
          n = 9 - len(recomendaciones)
          id_juego = recomendar_top_n(id_usuario, interacciones, n)
          for dato in datos_juegos(id_juego):
              recomendaciones.append(dato)
        
    else:
        print("recomendador: lightfm", file=sys.stdout)
        id_juego = recomendar_lightfm(id_usuario, interacciones, clicks = clicks)

    recomendaciones = datos_juegos(id_juego)   

    if len(recomendaciones) == 0:
        print("recomendador: top_9_no_jugo_a_nada", file=sys.stdout)
        id_juego = recomendar_top_9_no_jugo_a_nada(id_usuario, interacciones)
        recomendaciones = datos_juegos(id_juego)

    return  recomendaciones



if __name__ == '__main__':

  '''
  Modelo Light FM solo con datos de interacciones
  '''
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

  '''
  Modelo Light FM con datos de cada juego
  '''
  '''
  conn = dsrc.create_connection('Videojuegos.db')

  df_reviews = pd.read_sql_query(f"SELECT * FROM reviews", conn)

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
  (interactions_dl, weights_dl) = ds_details.build_interactions(df_reviews[["id_usuario", "id_juego", "Positive_rate"]].itertuples(index=False))

  (train_dl, test_dl) = lfm.cross_validation.random_train_test_split(interactions_dl, test_percentage=0.2, random_state=110293)
  (train_w_dl, test_w_dl) = lfm.cross_validation.random_train_test_split(weights_dl, test_percentage=0.2, random_state=110293)
  
  components = [10]
  ks = [1]
  ns = [1]
  learning_rates = [0.03]
  rhos = [0.9]
  epsilons = [1e-06]
  item_alphas = [0.0]
  user_alphas = [0.1]
  epochs = [1000]

  desde_aca = False

  if os.path.exists('./Hiperparametros_tuning.csv'):
     hp_tuning = pd.read_csv('./Hiperparametros_tuning.csv', sep=";")
  else:
     hp_tuning = pd.DataFrame(columns=['no_components','k','n','learning_rate','rho','epsilon','item_alpha','user_alpha','epoch','resultado'])
     desde_aca = True

  last_hp = hp_tuning.tail(1)

  resultado_mas_alto = 0

  mejores_features = []

  i = 1 

  i_total = len(components) * len(ks) * len(ns) * len(learning_rates) * len(rhos) * len(epsilons) * len(item_alphas) * len(user_alphas) * len(epochs)

  #TODO: Reemplazar por gridsearch

  for n in ns:
     for k in ks:
        for no_components in components:
           for learning_rate in learning_rates:
              for rho in rhos:
                 for epsilon in epsilons:
                    for item_alpha in item_alphas:
                       for user_alpha in user_alphas:
                          for epoch in epochs:
                            if last_hp.shape[0] == 1:
                              desde_aca = True
                              #if no_components == last_hp['no_components'].iloc[0] and k == last_hp['k'].iloc[0] and n == last_hp['n'].iloc[0] and learning_rate == last_hp['learning_rate'].iloc[0] and rho == last_hp['rho'].iloc[0] and epsilon == last_hp['epsilon'].iloc[0] and item_alpha == last_hp['item_alpha'].iloc[0] and user_alpha == last_hp['user_alpha'].iloc[0] and epoch == last_hp['epoch'].iloc[0]:
                              #  desde_aca = True

                            if desde_aca:
                              print(f'{i/i_total} - {i} /  {i_total}')

                              i += 1
                 
  #model_dl = lfm.LightFM(no_components=10, k=5, n=20, learning_schedule='adagrad', loss='logistic', learning_rate=0.05, rho=0.95, epsilon=1e-06, item_alpha=0.0, user_alpha=0.0, max_sampled=10, random_state=110293)
                              model_dl = lfm.LightFM(no_components=no_components, k=k, n=n, learning_schedule='adagrad', loss='logistic', learning_rate=learning_rate,item_alpha=item_alpha, user_alpha=user_alpha, max_sampled=10, random_state=110293)
  #model_dl.fit(train_dl, sample_weight=train_w_dl, item_features=game_features_build, epochs=100)
                              model_dl.fit(train_dl, sample_weight=train_w_dl, item_features=game_features_build, epochs=epoch)
                              resultado = lfm.evaluation.precision_at_k(model_dl, test_dl,k=k, num_threads=2, item_features=game_features_build).mean()
                            
                              new_row = {'no_components':no_components,
                              'k':k,
                              'n':n,
                              'learning_rate':learning_rate,
                              'rho':rho,
                              'epsilon':epsilon,
                              'item_alpha':item_alpha,
                              'user_alpha':user_alpha,
                              'epoch':epoch,
                              'resultado':resultado}
                              
                              
                              hp_tuning = pd.concat([hp_tuning, pd.DataFrame([new_row])], ignore_index=True)

                              hp_tuning.to_csv('./Hiperparametros_tuning.csv',sep=";",index=False)

                              if resultado > resultado_mas_alto:
                                resultado_mas_alto = resultado
                                mejores_features = [no_components,k,n,learning_rate,rho,epsilon,item_alpha,user_alpha,epoch]
                                print('------------------------------------------')
                                print(f'Features: no_components = {no_components}\n  k = {k}\n n = {n}\n learning_rate = {learning_rate}\n rho = {rho}\n epsilon = {epsilon}\n item_alpha = {item_alpha}\n user_alpha = {user_alpha}\n epoch = {epoch}\n Resultado: {resultado}')

  print(f'Mejor resultado: {resultado_mas_alto} \n Features {mejores_features} ')

'''

recomendacion = recomendar("ventevente")

recomendacion.append("1")

print(len(recomendacion))


  