from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

MSG_NOT_FOUND = 'Não encontrado.'
MSG_NO_DATA = 'Dados não informados'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///backend.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)


# Modelos de banco de dados
class Receitas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(255), unique=True, nullable=False)
    valor = db.Column(db.Float, nullable=False)
    data = db.Column(db.DateTime, server_default=db.func.current_timestamp(), 
                        server_onupdate=db.func.current_timestamp(), nullable=False)

    def __repr__(self):
        return f'<Receita {id}'


class Despesas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(255), unique=True, nullable=False)
    valor = db.Column(db.Float, nullable=False)
    data = db.Column(db.DateTime, server_default=db.func.current_timestamp(), 
                        server_onupdate=db.func.current_timestamp(), nullable=False)

    def __repr__(self):
        return f'<Despesa {id}'


# Esquemas da API
class ReceitasSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Receitas
    

class DespesasSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Despesas


receita_schema = ReceitasSchema()
receitas_schema = ReceitasSchema(many=True)

despesa_schema = DespesasSchema()
despesas_schema = DespesasSchema(many=True)


@app.route('/api/receitas', methods=['GET'])
def get_receitas():
    todas_receitas = Receitas.query.all()
    if todas_receitas:
        return jsonify(receitas_schema.dump(todas_receitas)), 200
    else:
        return jsonify({
            'Mensagem': MSG_NOT_FOUND   
        }), 404


@app.route('/api/receitas', methods=['POST'])
def post_receitas():
    descricao = request.json.get('descricao', '')
    valor = request.json.get('valor', '')

    receita = Receitas(
        descricao=descricao, 
        valor=valor
    )

    try:
        db.session.add(receita)
        db.session.commit()
    except:
        db.session.rollback()

    return jsonify(receita_schema.dump(receita)), 201


if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0',
        port='5500'
    )
