from multiprocessing import Process
from faceContrast.db import DBClient
import numpy as np
import face_recognition
import os

def getData():
    indexAndPath = {}
    indexs = []
    paths = []
    con = DBClient()
    datas = con.get()
    for data in datas:
        indexs.append(data[0])
        paths.append(data[1])
    indexAndPath['index'] = indexs
    indexAndPath['path'] = paths

    return indexAndPath


def face_2_matrix(file_paths):
    """
    将图片转化为矩阵类型，并提取人脸特征值，存储成*.out类型文件
    """
    num = 0
    for filePath in file_paths:
        path = filePath.split('.')[0]+".out"
        print(filePath)
        print(path)
        # try:
        obj = face_recognition.face_encodings(face_recognition.load_image_file(filePath))[0]
        print('ok')
        # except:
        #     continue
        if os.path.exists(path):
            print("该文件已存在")
            continue
        else:
            np.savetxt(path, obj)
        print(num)
        num += 1
    pass

class Schedule(object):

    @staticmethod
    def photo2Vector():
        """
        图像转换为矩阵类型
        """
        r = getData()
        face_2_matrix(r['path'])

        print(r)
        

    def run(self):
        print('photo2vector processing running')
        photo2vector_process = Process(target=Schedule.photo2Vector)
        # check_process = Process(target=Schedule.check_pool)
        photo2vector_process.start()
        # check_process.start()
