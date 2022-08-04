from api import app, db
from flask import Blueprint, jsonify, request
from sqlalchemy import extract, func
from api.models import Despesas
from api.schemas import despesas_schema, despesa_schema
from datetime import datetime

MSG_NOT_FOUND = app.config.get('MSG_NOT_FOUND')
MSG_NO_DATA = app.config.get('MSG_NO_DATA')
MSG_EMPTY_FIELD = app.config.get('MSG_EMPTY_FIELD')
FORMATO_DATA = app.config.get('FORMATO_DATA')
REGISTRO_EXISTE = app.config.get('REGISTRO_EXISTE')

despesas_api = Blueprint('despesas_api', __name__)


@despesas_api.route('/api/despesas', methods=['GET'])
def get_despesas():
    todas_despesas = Despesas.query.all()
    if todas_despesas:
        return jsonify(despesas_schema.dump(todas_despesas))
    else:
        return jsonify({
            'Mensagem': MSG_NOT_FOUND   
        }), 404


@despesas_api.route('/api/despesas', methods=['POST'])
def post_despesas():
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

    despesa = Despesas.query.filter(
        func.lower(Despesas.descricao) == descricao.lower()
    ).filter(
        extract('month', Despesas.data) == data.month,
        extract('year', Despesas.data) == data.year
    ).first()

    if despesa:
        return jsonify({
            'mensagem': REGISTRO_EXISTE
        })
    else:
        despesa = Despesas(
            descricao=descricao, 
            valor=valor,
            data=data
        )
        try:
            db.session.add(despesa)
            db.session.commit()
        except:
            db.session.rollback()
    return jsonify(despesa_schema.dump(despesa))


@despesas_api.route('/api/despesas/<int:id>', methods=['GET'])
def get_despesa(id):
    despesa = Despesas.query.get(id)
    if despesa:
        return jsonify(despesa_schema.dump(despesa))
    else:
        return jsonify({
            'Mensagem': MSG_NOT_FOUND   
        }), 404


@despesas_api.route('/api/despesas/<int:id>', methods=['PUT'])
def put_despesa(id):
    despesa = Despesas.query.get(id)
    if despesa:
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
                despesa.descricao = descricao
                despesa.valor = valor
                despesa.data = data
                db.session.commit()
            except:
                db.session.rollback()
        return jsonify(despesa_schema.dump(despesa))
    else:
        return jsonify({
            'Mensagem': MSG_NOT_FOUND   
        }), 404


@despesas_api.route('/api/despesas/<int:id>', methods=['DELETE'])
def del_despesa(id):
    despesa = Despesas.query.get(id)
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