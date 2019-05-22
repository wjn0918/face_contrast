# 允许上传的图片类型
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}



# 图像数据存储库信息[目前支持mysql(1),达梦(0)]
DB_FLAG = 1

MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_USER_NAME = 'root'
MYSQL_PASSWORD = 123456
MYSQL_DB_NAME = 'dm'

DM_HOST = '10.205.246.51'
DM_PORT = 5236
DM_USER_NAME = 'SYSDBA'
DM_PASSWORD =  'SYSDBA'




# mongodb配置
MONGODB_HOST = '192.168.2.221'
MONGODB_PORT = 27017



# 是否启用多进程初始化【1 开启，0 关闭】 多进程未开发成功
IF_PROGRESS = 1


# 相似度阀值
FACE_DISTANCE = 0.5


