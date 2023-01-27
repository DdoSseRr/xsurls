from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from flask_login import LoginManager
#from flask_sessionstore import Session
#from flask_session_captcha import FlaskSessionCaptcha,ImageCaptcha
import flask_qrcode



app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///userlinks.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

QRcode = flask_qrcode.QRcode(app)
db = SQLAlchemy(app)

from sweater import models, routes
