import sqlite3
import os 


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    os.chdir(os.path.dirname(__file__))
    
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def sql_select(query:str, con:sqlite3=None, params=None):

    if con == None:
        return print(f"\n ERROR: \n \tPrimero correr \033[;36m create_connection() \033[0m para realizar la conexión")
    
    con.row_factory = sqlite3.Row # esto es para que devuelva registros en el fetchall
    cur = con.cursor()

    if params:
        res = cur.execute(query, params)
    else:
        res = cur.execute(query)
    
    ret = res.fetchall()
    con.close()

    return ret

def sql_execute(query:str, con:sqlite3=None, params=None):
    
    if con == None:
        return print(f"\n ERROR: \n \tPrimero correr \033[;36m create_connection() \033[0m para realizar la conexión")
    
    cur = con.cursor()    
    
    if params:
        res = cur.execute(query, params)
    else:
        res = cur.execute(query)
    
    con.commit()
    con.close()
    
    return print(f'\n Query ejecutada \n')

if __name__ == '__main__':
    
    '''
    query = f"INSERT INTO interacciones (id_interaccion, id_juego, id_usuario, rating) VALUES (?, ?, ?, ?) ON CONFLICT (id_interaccion) DO UPDATE SET rating=?;" # si el rating existia lo actualizo
    params = ('red-dead-redemption-2OVLange', 'red-dead-redemption-2', 'OVLange', 10, 10)
    conn = create_connection('Videojuegos.db')
    sql_execute(query, con=conn, params=params)
    '''
    query = f"SELECT * FROM reviews" # si el rating existia lo actualizo
    #params = ('red-dead-redemption-2OVLange', 'red-dead-redemption-2', 'OVLange', 10, 10)
        
    os.chdir(os.path.dirname(__file__))
    
    conn = create_connection('Videojuegos.db')
    
    res = sql_select(query, con=conn)
