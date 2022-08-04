from lib2to3.pytree import Base
from flask import Flask
from api.config import BaseConfig
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config.from_object(BaseConfig)

db = SQLAlchemy(app)
ma = Marshmallow(app)


# Cria banco de dados
@app.before_first_request
def cria_db():
    db.create_all()