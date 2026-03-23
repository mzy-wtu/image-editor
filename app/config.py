import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    # 使用MySQL数据库
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost:3306/image_editor'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOGIN_REMEMBER_DURATION = timedelta(days=7)
