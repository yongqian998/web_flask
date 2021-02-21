"""
author:liuyongqian
date: 2020-12-20
"""
import os
HOST = "192.168.100.1"
PORT = 3000
DEBUG = True

# 配置数据库的连接
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:Sanchuang123#@121.4.100.38:3306/web_proj"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY=os.urandom(24)

CMS_USER_ID="ASDFGH"
FRONT_USER_ID='SDGHHJKJU'
# MAIL_USE_TLS：端口号587
# MAIL_USE_SSL：端口号465
# QQ邮箱不支持非加密方式发送邮件
# 发送者邮箱的服务器地址
MAIL_SERVER = "smtp.qq.com"
MAIL_PORT = '587'
MAIL_USE_TLS = True
# MAIL_USE_SSL
MAIL_USERNAME = "1066702610@qq.com"
MAIL_PASSWORD = "plrjrehnnkhhbeah"
MAIL_DEFAULT_SENDER = "1066702610@qq.com"

# celery相关的配置
# CELERY_RESULT_BACKEND = "redis://121.4.100.38:6379/0"
# CELERY_BROKER_URL = "redis://121.4.100.38:6379/0"
# flask-paginate的相关配置
PER_PAGE = 10
