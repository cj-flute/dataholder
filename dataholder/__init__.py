from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = '68dbd4ebada65d0e9a120046a3134590'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dataholder.db'
db = SQLAlchemy(app)  # noqa

from dataholder import route  # noqa
