import os
from dotenv import load_dotenv

load_dotenv()

class BaseConfig:
    """基础配置"""
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key-change-in-production"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    IMAGE_UPLOAD_FOLDER = os.environ.get("IMAGE_UPLOAD_FOLDER", "./images")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

class DevelopmentConfig(BaseConfig):
    """开发环境配置"""
    DEBUG = True
    DB_TYPE = os.environ.get("DB_TYPE", "sqlite")
    
    if DB_TYPE == "mysql":
        DB_HOST = os.environ.get("DB_HOST", "localhost")
        DB_PORT = os.environ.get("DB_PORT", "3306")
        DB_NAME = os.environ.get("DB_NAME", "image_editor")
        DB_USER = os.environ.get("DB_USER", "root")
        DB_PASSWORD = os.environ.get("DB_PASSWORD", "123456")
        SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    else:
        DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "instance", "image_editor.db")
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH}"

class ProductionConfig(BaseConfig):
    """生产环境配置"""
    DEBUG = False
    DB_HOST = os.environ.get("DB_HOST", "localhost")
    DB_PORT = os.environ.get("DB_PORT", "3306")
    DB_NAME = os.environ.get("DB_NAME", "image_editor")
    DB_USER = os.environ.get("DB_USER", "root")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "123456")
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# 根据环境变量选择配置
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": ProductionConfig
}

def get_config():
    env = os.environ.get("FLASK_ENV", "production")
    return config.get(env, config["default"])
