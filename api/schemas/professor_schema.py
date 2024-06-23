from api import ma
from ..models import professor_model
from marshmallow import fields


class ProfessorSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = professor_model.Professor
        load_instance = True
        fields = ('id', 'nome', 'idade', '_links')

    nome = fields.String(required=True)
    idade = fields.Integer(required=True)

    _links = ma.Hyperlinks(
        {
            'get': ma.URLFor('professordetail', values={'id': '<id>'}),
            'put': ma.URLFor('professordetail', values={'id': '<id>'}),
            'delete': ma.URLFor('professordetail', values={'id': '<id>'})
        }
    )
