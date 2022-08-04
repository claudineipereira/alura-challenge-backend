from api import app
from api import ma
from api.models import Receitas

FORMATO_DATA = app.config.get('FORMATO_DATA')


class ReceitasSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Receitas
        dateformat = FORMATO_DATA


receita_schema = ReceitasSchema()
receitas_schema = ReceitasSchema(many=True)