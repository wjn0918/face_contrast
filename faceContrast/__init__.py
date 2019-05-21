# import multiprocessing as mp
# import face_recognition
# import time

# def job(x):
#     print(x)
#     # # print("******")
#     r = None
#     # try:
#     #     r = face_recognition.face_encodings(face_recognition.load_image_file(x))[0]
#     # except:
#     #     print('error')
#     time.sleep(2)

#     return r


# def multicore(datas):
#     pool=mp.Pool(processes=2)#定义一个Pool，并定义CPU核数量为2
#     res=pool.map(job,datas['path'])

#     pool.close()
#     pool.join()
#     print(res)
#     print("*"*10)
#     print(i.get() for i in res)
# 
# if __name__=='__main__':
#     datas = {'index': ['123456', '1', '1', '1', '1', '2', '3'], 'path': ['C:\\\\Users\\\\EDZ\\\\Desktop\\\\1.jpg', 'D:softdlibdlib-masterexamplesjohnsJohn_Salley1.jpg', 'D:softdlibdlib-masterexamplesjohnsJohn_Salley2.jpg', 'D:softdlibdlib-masterexamplesjohnsJohn_Salley3.jpg', 'D:/soft/dlib/dlib-master/examples/johns/John_Salley/1.jpg', 'D:/soft/dlib/dlib-master/examples/johns/John_Salley/2.jpg', 'D:/soft/dlib/dlib-master/examples/johns/John_Salley/3.jpg']}

#     multicore(datas)
