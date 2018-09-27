import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from config import basedir, ADMINS, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD
from flask.ext.mail import Mail
from flask.ext.httpauth import HTTPBasicAuth
from itsdangerous import URLSafeTimedSerializer

app = Flask(__name__)
app.config.from_object('config')

auth = HTTPBasicAuth()

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

login_serializer = URLSafeTimedSerializer(app.secret_key)

mail = Mail(app)

from app import views, models, api