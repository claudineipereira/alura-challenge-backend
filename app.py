from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///backend.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Receitas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(255), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    data = db.Column(db.DateTime, server_default=db.func.current_timestamp(), 
                        server_onupdate=db.func.current_timestamp(), nullable=False)

    def __repr__(self):
        return f'<Receita {id}'


class Despesas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(255), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    data = db.Column(db.DateTime, server_default=db.func.current_timestamp(), 
                        server_onupdate=db.func.current_timestamp(), nullable=False)

    def __repr__(self):
        return f'<Despesa {id}'


@app.route('/')
def index():
    return 'Olá!'


if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0',
        port='5500'
    )
