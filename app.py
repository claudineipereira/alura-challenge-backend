from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

MSG_NOT_FOUND = 'Não encontrado.'
MSG_NO_DATA = 'Dados não informados'
MSG_EMPTY_FIELD = 'Requisição incompleta'

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


# Rotas de receitas
@app.route('/api/receitas', methods=['GET'])
def get_receitas():
    todas_receitas = Receitas.query.all()
    if todas_receitas:
        return jsonify(receitas_schema.dump(todas_receitas))
    else:
        return jsonify({
            'Mensagem': MSG_NOT_FOUND   
        })


@app.route('/api/receitas', methods=['POST'])
def post_receitas():
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
        receita = Receitas.query.filter_by(descricao=descricao).first()

        if not receita:
            receita = Receitas(
                descricao=descricao, 
                valor=valor
            )

            try:
                db.session.add(receita)
                db.session.commit()
            except:
                db.session.rollback()

        return jsonify(receita_schema.dump(receita))


@app.route('/api/receitas/<int:id>', methods=['GET'])
def get_receita(id):
    receita = Receitas.query.get_or_404(id)
    if receita:
        return jsonify(receita_schema.dump(receita))
    else:
        return jsonify({
            'Mensagem': MSG_NOT_FOUND   
        }), 404


@app.route('/api/receitas/<int:id>', methods=['PUT'])
def put_receita(id):
    receita = Receitas.query.get_or_404(id)
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
    receita = Receitas.query.get_or_404(id)
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


# Rotas de despesas
@app.route('/api/despesas', methods=['GET'])
def get_despesas():
    todas_receitas = Despesas.query.all()
    if todas_receitas:
        return jsonify(despesas_schema.dump(todas_receitas))
    else:
        return jsonify({
            'Mensagem': MSG_NOT_FOUND   
        })


@app.route('/api/despesas', methods=['POST'])
def post_despesas():
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
        despesa = Despesas.query.filter_by(descricao=descricao).first()

        if not despesa:
            despesa = Despesas(
                descricao=descricao, 
                valor=valor
            )

            try:
                db.session.add(despesa)
                db.session.commit()
            except:
                db.session.rollback()

        return jsonify(despesa_schema.dump(despesa))


@app.route('/api/despesas/<int:id>', methods=['GET'])
def get_despesa(id):
    despesa = Despesas.query.get_or_404(id)
    if despesa:
        return jsonify(despesa_schema.dump(despesa))
    else:
        return jsonify({
            'Mensagem': MSG_NOT_FOUND   
        }), 404


@app.route('/api/despesas/<int:id>', methods=['PUT'])
def put_despesa(id):
    despesa = Despesas.query.get_or_404(id)
    if despesa:
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
                despesa.descricao = descricao
                despesa.valor = valor
                db.session.commit()
            except:
                db.session.rollback()

            return jsonify(despesa_schema.dump(despesa))
    else:
        return jsonify({
            'Mensagem': MSG_NOT_FOUND   
        }), 404


@app.route('/api/despesas/<int:id>', methods=['DELETE'])
def del_despesa(id):
    despesa = Despesas.query.get_or_404(id)
    if despesa:
        try:
            db.session.delete(despesa)
            db.session.commit()
        except:
            db.session.rollback()
        return jsonify(despesa_schema.dump(despesa))
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
