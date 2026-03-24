from flask import Flask
from flask_login import LoginManager
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('app.config.Config')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

CORS(app, origins=['http://localhost:5173', 'http://47.121.190.137:5173', 'http://47.121.190.137:5000'], supports_credentials=True)

db = SQLAlchemy(app)

from app import routes
from app.models.user import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
