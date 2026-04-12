import os
from flask import Flask
from flask_login import LoginManager
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('app.config.Config')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# CORS origins: 从环境变量读取，多个用逗号分隔
_cors_origins = os.environ.get(
    'ALLOWED_ORIGINS',
    'http://localhost:5173,http://localhost:5000'
).split(',')
CORS(app, origins=_cors_origins, supports_credentials=True)

db = SQLAlchemy(app)

from app import routes
from app.models.user import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
