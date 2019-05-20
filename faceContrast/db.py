
from DBUtils.PooledDB import PooledDB
from faceContrast.settings import * 
import pymysql
from pymongo import MongoClient
from bson.binary import Binary

import pickle

   
class MongoDBClient(object):

    def __init__(self):
        self.con = MongoClient(host=MONGODB_HOST, port=MONGODB_PORT)
        self.db = self.con.face_recognition


    def set(self,obj: dict):
        """
        插入数据
        @param obj：字典类型，k：身份id,v：人像特征数据
        """
        collection = self.db.faces_set
        collection.insert({'id':obj['id'], 'facedata': Binary(pickle.dumps(obj['facedata'],protocol=-1),subtype=128)})

    def get(self) -> dict:
        """
        获取mongodb中的数据并以字典形式返回
        """
        collection = self.db.faces_set
        datas = collection.find()
        id_facedata = {}
        ids = []
        facedatas = []
        for data in datas:
            ids.append(data['id'])
            facedatas.append(pickle.loads(data['facedata']))
        id_facedata['id'] = ids
        id_facedata['facedata'] = facedatas
        return id_facedata


class MysqlClient(object):

    def __init__(self):
        self.pool = PooledDB(pymysql, 5, host=MYSQL_HOST, user=MYSQL_USER_NAME, passwd=str(MYSQL_PASSWORD), db=MYSQL_DB_NAME, port=MYSQL_PORT, setsession=['SET AUTOCOMMIT = 1'])
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
    c = MongoDBClient()
    
