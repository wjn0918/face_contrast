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






# 特征数据存储位置【1：mongodb,0:本地】
DATA_SAVE_LOCATION = 1

# mongodb配置
MONGODB_HOST = '10.205.246.34'
MONGODB_PORT = 27017



# 使用进程数，提高性能
PROGRESS_NUMBER = 4

