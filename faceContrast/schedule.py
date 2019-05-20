from multiprocessing import Process
from faceContrast.db import MysqlClient, MongoDBClient, DMClient
import numpy as np
import face_recognition
import os
from faceContrast.settings import * 
from apscheduler.schedulers.background import BackgroundScheduler
import logging


if os.path.exists('log'):
    pass   
else:
    os.mkdir('log')


logging.basicConfig(level=logging.DEBUG,#控制台打印的日志级别
                filename='log/run.log',
                filemode='a',##模式，w写模式，a是追加模式，默认如果不写的话，就是追加模式
                format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s', #日志格式
                )



def getData(flag:int):
    indexAndPath = {}
    indexs = []
    paths = []
    if DB_FLAG:
        con = MysqlClient()
    else:
        con = DMClient()
    datas = con.get(flag)
    for data in datas:
        indexs.append(data[0])
        paths.append(data[1])
    indexAndPath['index'] = indexs
    indexAndPath['path'] = paths

    return indexAndPath


def save2mongo(obj: dict):
    """
    特征数据存储到mongodb
    """
    con = MongoDBClient()
    con.set(obj)



    pass

def save2local(path:str, obj: dict):
    if os.path.exists(path):
        print("该文件已存在")
    else:
        np.savetxt(path, obj['facedata'])


def face_2_matrix(datas: dict):
    """
    将图片转化为矩阵类型，并提取人脸特征值，存储成*.out类型文件
    """
    for index, filePath in enumerate(datas['path']):
        id_facedata = {}
        path = filePath.split('.')[0]+".out"
        id_facedata['id'] = datas['index'][index]
        try:
            obj = face_recognition.face_encodings(face_recognition.load_image_file(filePath))[0]
            id_facedata['facedata'] = obj
        except FileNotFoundError:
            print("No such file or directory: %s" %(filePath))
            logging.error("id_number:%s, No such file or directory: %s " %(datas['index'][index], filePath))
            continue
        except IndexError:
            print("don't have face in this photo")
            logging.error("id_number:%s, don't have face in this photo: %s " %(datas['index'][index], filePath))
            continue
        if DATA_SAVE_LOCATION == 1:
            save2mongo(id_facedata)
        if DATA_SAVE_LOCATION == 0:
            save2local(path, id_facedata)


        
    pass

class Schedule(object):

    @staticmethod
    def photo2Vector_all():
        """
        图像转换为矩阵类型
        全量数据更新
        """
        r = getData(1)
        face_2_matrix(r)
        print(r)


    @staticmethod
    def photo2Vector_add():
        """
        图像转换为矩阵类型
        增量数据更新
        """
        r = getData(0)
        face_2_matrix(r)
        print(r)

    
  
    @staticmethod
    def getfacedatas():
        """
        获取mongodb中的人像特征数据
        """
        con = MongoDBClient()
        id_facedata = con.get()
        print(id_facedata)

        
        

    def run(self):
        """

        """
        # 全量数据转换
        photo2vector_process = Process(target=Schedule.photo2Vector_all)
        photo2vector_process.start()

        # 增量数据定时执行
        scheduler = BackgroundScheduler()
        # 间隔3秒钟执行一次
        scheduler.add_job(Schedule.photo2Vector_add, 'interval', seconds=100000)
        # 定时任务12:00执行
        # scheduler.add_job(Schedule.photo2Vector, 'cron', hour=24, minute=0)
        # 这里的调度任务是独立的一个线程
        scheduler.start()
        # print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

        # print('photo2vector processing running')
        # photo2vector_process = Process(target=Schedule.photo2Vector)
        # photo2vector_process.start()

        # print('getfacedatas processing running')
        # getfacedatas = Process(target=Schedule.getfacedatas)
        # getfacedatas.start()




    

        


