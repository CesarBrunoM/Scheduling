from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = '6025524ac8f6491f7d860090f8e77a47'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/systembd'

database = SQLAlchemy(app)

from indoc import routes
