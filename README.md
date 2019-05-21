# face_contrast
人脸对比


1、全量获取数据库中人像信息进行特征提取并批量存储到mongodb
2、每日增量获取人像信息进行特征提取并存储到mongodb

返回数据：
    distance【图像相似度】
    id【id_number】
    [{'distance': , 'id': },{'distance': , 'id': }]



需要解决：
1、性能优化，初始化数据太慢[V]
2、获取数据库中人像数据的形式[V]
3、日志按时间，按大小进行文件切分

