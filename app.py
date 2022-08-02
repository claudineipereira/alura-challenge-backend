from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime

MSG_NOT_FOUND = 'Não encontrado.'
MSG_NO_DATA = 'Dados não informados'
MSG_EMPTY_FIELD = 'Requisição incompleta'
FORMATO_DATA = '%d/%m/%Y'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///backend.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)


# Modelos de banco de dados
class Receitas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(255), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    data = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'<Receita {id}'


class Despesas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(255), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    data = db.Column(db.DateTime, nullable=False)

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


# Rotas de receitas
@app.route('/api/receitas', methods=['GET'])
def get_receitas():
    todas_receitas = Receitas.query.all()
    if todas_receitas:
        return jsonify(receitas_schema.dump(todas_receitas))
    else:
        return jsonify({
            'Mensagem': MSG_NOT_FOUND   
        }), 404


@app.route('/api/receitas', methods=['POST'])
def post_receitas():
    descricao = request.json.get('descricao')
    valor = request.json.get('valor')
    data = request.json.get('data')

    if descricao is None and valor is None and data is None:
        return jsonify({
            'Mensagem': MSG_NO_DATA
        }), 204   

    if descricao is None or valor is None or data is None:
        return jsonify({
            'Mensagem': MSG_EMPTY_FIELD
        }), 204          
    
    data = datetime.strptime(data, FORMATO_DATA)
    receita = Receitas.query.filter_by(
        descricao=descricao,
        data=data
    ).first()

    if not receita:
        receita = Receitas(
            descricao=descricao, 
            valor=valor,
            data=data
        )

        try:
            db.session.add(receita)
            db.session.commit()
        except:
            db.session.rollback()

    return jsonify(receita_schema.dump(receita))


@app.route('/api/receitas/<int:id>', methods=['GET'])
def get_receita(id):
    receita = Receitas.query.get(id)
    if receita:
        return jsonify(receita_schema.dump(receita))
    else:
        return jsonify({
            'Mensagem': MSG_NOT_FOUND   
        }), 404


@app.route('/api/receitas/<int:id>', methods=['PUT'])
def put_receita(id):
    receita = Receitas.query.get(id)
    if receita:
        descricao = request.json.get('descricao')
        valor = request.json.get('valor')

        if descricao is None and valor is None:
            return jsonify({
                'Mensagem': MSG_NO_DATA
            }), 204
        elif descricao is None or valor is None:
            return jsonify({
                'Mensagem': MSG_EMPTY_FIELD
            }), 204
        else:
            try:
                receita.descricao = descricao
                receita.valor = valor
                db.session.commit()
            except:
                db.session.rollback()

            return jsonify(receita_schema.dump(receita))
    else:
        return jsonify({
            'Mensagem': MSG_NOT_FOUND   
        }), 404


@app.route('/api/receitas/<int:id>', methods=['DELETE'])
def del_receita(id):
    receita = Receitas.query.get(id)
    if receita:
        try:
            db.session.delete(receita)
            db.session.commit()
        except:
            db.session.rollback()
        return jsonify(receita_schema.dump(receita))
    else:
        return jsonify({
            'Mensagem': MSG_NOT_FOUND   
        }), 404



if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0',
        port='5500'
    )
