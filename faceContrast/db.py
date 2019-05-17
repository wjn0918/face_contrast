
from DBUtils.PooledDB import PooledDB
from faceContrast.settings import * 
import pymysql

   



class DMClient(object):
    def __init__(self, host=HOST, port=PORT):
        if PASSWORD:
            self._db = redis.Redis(host=host, port=port, password=PASSWORD)
        else:
            self._db = redis.Redis(host=host, port=port)



class DBClient(object):

    def __init__(self):
        if DB_TYPE == 'mysql':
            self.pool = PooledDB(pymysql, 5, host=HOST, user=USER_NAME, passwd=str(PASSWORD), db=DB_NAME, port=PORT, setsession=['SET AUTOCOMMIT = 1'])
    def get(self):
        con = self.pool.connection()
        cursor = con.cursor()
        sql = 'select * from t_face_recognition'
        cursor.execute(sql)
        datas = cursor.fetchall()
        cursor.close()
        con.close()
        return datas


if __name__ == '__main__':
    c = DBClient()
    c.get()
    
