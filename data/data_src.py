import sqlite3
import os 


class Data_source():

    def __init__(self, db_file):

        self.db_file = db_file
    
    def create_connection(self, db_file):
        """ create a database connection to the SQLite database
            specified by the db_file
        :param db_file: database file
        :return: Connection object or None
        """
        os.chdir(os.path.dirname(__file__))
    
        conn = None
        try:
            conn = sqlite3.connect(db_file, check_same_thread=False)
        except Error as e:
            print(e)
    
        return conn

    def sql_select(self, query:str, params=None):

        con = self.create_connection(self.db_file)

        con.row_factory = sqlite3.Row # esto es para que devuelva registros en el fetchall
        cur = con.cursor()

        if params:
            res = cur.execute(query, params)
        else:
            res = cur.execute(query)

        ret = res.fetchall()
        con.close()

        return ret

    def sql_execute(self, query:str, params=None):

        con = self.create_connection(self.db_file)

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

    data_scr = Data_source('Videojuegos.db')
    
    res = data_scr.sql_select(query)

    print(res)
