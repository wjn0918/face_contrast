
from DBUtils.PooledDB import PooledDB
from faceContrast.settings import * 
import pymysql
from pymongo import MongoClient
from bson.binary import Binary
import datetime
import pickle
# import dmPython
import logging

   
class MongoDBClient(object):

    def __init__(self):
        self.con = MongoClient(host=MONGODB_HOST, port=MONGODB_PORT)
        self.db = self.con.face_recognition


    def insert(self,obj: list):
        """
        插入数据
        @param obj：字典类型，k：身份id,v：人像特征数据
        """
        collection = self.db.faces_set
        # collection.insert({'id':obj['id'], 'facedata': Binary(pickle.dumps(obj['facedata'],protocol=-1),subtype=128)})
        collection.insert(obj)

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

    def get(self,flag: int):
        """
        获取数据
        @param flag:判断数据获取方式 1 全量数据， 0 增量数据
        """
        today =datetime.datetime.now().date()

        con = self.pool.connection()
        cursor = con.cursor()
        if flag:
            sql = 'select * from t_face_recognition'
            args = None
            print("获取全量数据")
            logging.info("initial, encoding all data")
        else:
            sql = 'select * from t_face_recognition where DATE(flag) = %s'
            args = today
            print("获取增量数据")
        cursor.execute(sql, args)
        datas = cursor.fetchall()
        cursor.close()
        con.close()
        return datas




class DMClient(object):

    def __init__(self):
        self.conn = dmPython.connect(host=DM_HOST,port=DM_PORT,user=DM_USER_NAME,password=DM_PASSWORD)

    def get(self,flag: int):
        """
        获取数据
        @param flag:判断数据获取方式 1 全量数据， 0 增量数据
        """
        today =datetime.datetime.now().date()

        
        cursor = self.conn.cursor()
        if flag:
            sql = 'select * from "SYSDBA"."T_CS_FACE_RECOGNITION"'
            # args = None
            print("获取全量数据")
            logging.info("initial, encoding all data")
        else:
            sql = 'select * from "SYSDBA"."T_CS_FACE_RECOGNITION" where to_date(update_time) = \'%s\'' %(today)
            # args = today
            print("获取增量数据")
        cursor.execute(sql)
        datas = cursor.fetchall()
        cursor.close()
        self.conn.close()
        return datas





if __name__ == '__main__':
    c = MongoDBClient()
    
