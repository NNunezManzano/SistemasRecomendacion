import sys
import json
import os 
from data.data_src import Data_source
dsrc = Data_source('Videojuegos.db')

def actualizador(query):    
    dsrc.sql_execute(query)
    return 

def datos_juegos(id_juego):
    query = f"SELECT DISTINCT * FROM juegos WHERE id_juego IN ({','.join(['?']*len(id_juego))})"
    juegos = dsrc.sql_select(query, id_juego)
    return juegos


query_create = """CREATE TABLE juegos_tmp as 
SELECT j.*, 
CASE
	WHEN j.Genero LIKE ('%RPG%') 	THEN 'RPG'
	WHEN j.Genero LIKE ('%strat%') 	THEN 'estrategia'
	WHEN j.Genero LIKE ('%tact%') 	THEN 'estrategia'
	WHEN j.Genero LIKE ('%shoot%') 	THEN 'shooter'
	WHEN j.Genero LIKE ('%sport%') 	THEN 'sport'
	WHEN j.Genero LIKE ('%soccer%') THEN 'sport'
	WHEN j.Genero LIKE ('%Basket%') THEN 'sport'
	WHEN j.Genero LIKE ('%vol%') 	THEN 'sport'
	WHEN j.Genero LIKE ('%golf%') 	THEN 'sport'
	WHEN j.Genero LIKE ('%adventure%') 	THEN 'accion'
	WHEN j.Genero LIKE ('%action%') 	THEN 'action'
	WHEN j.Genero LIKE ('%raci%') 	THEN 'carreras'	
	ELSE '	'	
    END as Sub_genero
    FROM juegos j;"""
actualizador(query_create)

query_drop = """DROP TABLE juegos;"""
actualizador(query_drop)

query_alter = """ALTER TABLE juegos_tmp RENAME TO juegos;"""
actualizador(query_alter)

datos = datos_juegos('rocket-league')

for dato in datos:
    print(dato)