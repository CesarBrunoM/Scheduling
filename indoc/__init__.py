from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.config['SECRET_KEY'] = '6025524ac8f6491f7d860090f8e77a47'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/systembd'

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from indoc import routes
