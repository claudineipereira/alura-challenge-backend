import os

basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'backend.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MSG_NOT_FOUND = 'Não encontrado'
    MSG_NO_DATA = 'Dados não informados'
    MSG_EMPTY_FIELD = 'Requisição incompleta'
    FORMATO_DATA = '%d/%m/%Y'
    REGISTRO_EXISTE = 'Entrada já existe neste mês e ano'