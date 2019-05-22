from multiprocessing import Process
from faceContrast.db import MysqlClient, MongoDBClient, DMClient
import numpy as np
import face_recognition
import os
from faceContrast.settings import * 
from apscheduler.schedulers.background import BackgroundScheduler
from multiprocessing import Pool
import multiprocessing
import time
from bson.binary import Binary
import pickle



import logging

if os.path.exists('logs'):
    pass
else:
    os.mkdir('logs')

logging.basicConfig(
                level=logging.DEBUG,#控制台打印的日志级别
                filename='logs/run.log',
                filemode='a',##模式，w写模式，a是追加模式，默认如果不写的话，就是追加模式
                format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s', #日志格式
                )



# 获取本机cpu核数
PROGRESS_NUMBER = multiprocessing.cpu_count()

def getData(flag:int) -> dict:
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
    con.insert(obj)
    print('over')




    pass

def save2local(path:str, obj: dict):
    """特征数据存储到本地"""
    if os.path.exists(path):
        print("该文件已存在")
    else:
        np.savetxt(path, obj['facedata'])


def extract_feature(filePath):
    """获取人像特征数据"""
    bin_facedata = ''
    try:
        r = face_recognition.face_encodings(face_recognition.load_image_file(filePath))[0]
        bin_facedata = Binary(pickle.dumps(r,protocol=-1),subtype=128)
    except IndexError:
        logging.error('there no face in this photo')
    except FileNotFoundError:
        logging.error('the file is not exits :' + filePath)
    except:
        print('error')
    return bin_facedata



def face_2_matrix(datas: dict):
    """
    将图片转化为矩阵类型，并提取人脸特征值进行存储
    """
    reduced_datas = []
    for index, filePath in enumerate(datas['path']):
        id_facedata = {}
        path = filePath.split('.')[0]+".out"
        id_facedata['id'] = datas['index'][index]
        obj = extract_feature(filePath)
        if obj != '':
            id_facedata['facedata'] = obj
        else:
            continue
        reduced_datas.append(id_facedata)
    if DATA_SAVE_LOCATION == 1:
        save2mongo(reduced_datas)
        print("存储成功")
    if DATA_SAVE_LOCATION == 0:
        save2local(path, id_facedata)        
    pass


def face_2_matrix_multi(datas: dict):
    """
    使用多进程将图片转化为矩阵类型，并提取人脸特征值进行存储
    """
    reduced_datas = []
    pool = Pool(PROGRESS_NUMBER)
    know_facings = pool.map(extract_feature, datas['path'])
    pool.close()#关闭进程池，不再接受新的进程
    pool.join()#主进程阻塞等待子进程的退出
    # print(know_facings)
    for index, obj in enumerate(know_facings):
        id_facedata = {}
        id_facedata['id'] = datas['index'][index]
        if obj != '':
            id_facedata['facedata'] = obj
        else:
            continue
        reduced_datas.append(id_facedata)
    save2mongo(reduced_datas)
    # print("存储成功")
    pass

class Schedule(object):

    @staticmethod
    def photo2Vector_all():
        """
        图像转换为矩阵类型
        全量数据更新
        """
        t1 = time.time()    
        datas = getData(1)
        # print(datas)
        if IF_PROGRESS:
            # print("开启多进程")
            face_2_matrix_multi(datas)
        else:
            face_2_matrix(datas)
        # t2 = time.time()
        # print ("并行执行时间：", int(t2-t1))



    @staticmethod
    def photo2Vector_add():
        """
        图像转换为矩阵类型
        增量数据更新
        """
        r = getData(0)
        face_2_matrix(r)
        # print(r)

    
  
    @staticmethod
    def getfacedatas():
        """
        获取mongodb中的人像特征数据
        """
        con = MongoDBClient()
        id_facedata = con.get()
        # print(id_facedata)

        
        

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

        print('getfacedatas processing running')
        getfacedatas = Process(target=Schedule.getfacedatas)
        getfacedatas.start()




    

        


