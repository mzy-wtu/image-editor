import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    DB_TYPE = os.environ.get('DB_TYPE', 'mysql')
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = os.environ.get('DB_PORT', '3306')
    DB_NAME = os.environ.get('DB_NAME', 'image_editor')
    DB_USER = os.environ.get('DB_USER', 'root')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', '123456')
    
    if DB_TYPE == 'mysql':
        SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    else:
        DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'instance', f'{DB_NAME}.db')
        SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_PATH}'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOGIN_REMEMBER_DURATION = timedelta(days=7)
    
    IMAGE_UPLOAD_FOLDER = os.environ.get('IMAGE_UPLOAD_FOLDER', './images')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
