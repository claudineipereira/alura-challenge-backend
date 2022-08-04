from api import app
from api import ma
from api.models import Receitas
from api.models import Despesas

FORMATO_DATA = app.config.get('FORMATO_DATA')


class ReceitasSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Receitas
        dateformat = FORMATO_DATA


receita_schema = ReceitasSchema()
receitas_schema = ReceitasSchema(many=True)


class DespesasSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Despesas
        dateformat = FORMATO_DATA


despesa_schema = DespesasSchema()
despesas_schema = DespesasSchema(many=True)