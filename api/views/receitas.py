from api import app, db
from flask import jsonify, request
from sqlalchemy import extract, func
from api.schemas.receitas import receitas_schema, receita_schema
from api.models.receitas import Receitas
from datetime import datetime


MSG_NOT_FOUND = app.config.get('MSG_NOT_FOUND')
MSG_NO_DATA = app.config.get('MSG_NO_DATA')
MSG_EMPTY_FIELD = app.config.get('MSG_EMPTY_FIELD')
FORMATO_DATA = app.config.get('FORMATO_DATA')
REGISTRO_EXISTE = app.config.get('REGISTRO_EXISTE')


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
    
    data = datetime.date(
        datetime.strptime(data, FORMATO_DATA)
    )

    receita = Receitas.query.filter(
        func.lower(Receitas.descricao) == descricao.lower()
    ).filter(
        extract('month', Receitas.data) == data.month,
        extract('year', Receitas.data) == data.year
    ).first()

    if receita:
        return jsonify({
            'mensagem': REGISTRO_EXISTE
        })
    else:
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
        data = request.json.get('data')

        if descricao is None and valor is None and data is None:
            return jsonify({
                'Mensagem': MSG_NO_DATA
            }), 204   
        elif descricao is None or valor is None or data is None:
            return jsonify({
                'Mensagem': MSG_EMPTY_FIELD
            }), 204          
        else:
            data = datetime.date(
                datetime.strptime(data, FORMATO_DATA)
            )
            try:
                receita.descricao = descricao
                receita.valor = valor
                receita.data = data
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
