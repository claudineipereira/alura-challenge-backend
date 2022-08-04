from flask import Flask
from config import BaseConfig
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config.from_object(BaseConfig)

db = SQLAlchemy(app)
ma = Marshmallow(app)

from api.views.receitas import receitas_api
from api.views.despesas import despesas_api

app.register_blueprint(receitas_api, url_prefix='/api')
app.register_blueprint(despesas_api, url_prefix='/api')

# Cria banco de dados
@app.before_first_request
def cria_db():
    db.create_all()