from multiprocessing import Process
from db import DBClient

def getData():
    con = DBClient()
    return con.get()

class Schedule(object):

    @staticmethod
    def photo2Vector():
        """
        图像转换为矩阵类型
        """
        r = getData()
        print(r)
        

    def run(self):
        print('Ip processing running')
        photo2Vector_process = Process(target=Schedule.photo2Vector)
        # check_process = Process(target=Schedule.check_pool)
        photo2Vector_process.start()
        # check_process.start()
