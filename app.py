from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
from datetime import timedelta
import os
from DBModels import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI', 'sqlite:///data.db')
db.init_app(app)
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')
Bootstrap5(app)

login_manager = LoginManager()
login_manager.init_app(app)

app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_PERMANENT'] = True

@login_manager.user_loader
def load_user(user_id):
    from DBModels import Users
    return db.get_or_404(Users, user_id)
