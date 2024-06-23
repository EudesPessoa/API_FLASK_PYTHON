from flask_restful import Resource
from api import api
from ..schemas import professor_schema
from flask import request, make_response, jsonify
from ..entidades import professor
from ..services import professor_service
from ..models.professor_model import Professor
from paginate import paginate
from flask_jwt_extended import jwt_required


class ProfessorList(Resource):
    @jwt_required()
    def get(self):
        # professores = professor_service.listar_professores()
        cs = professor_schema.ProfessorSchema(many=True)
        # return make_response(cs.jsonify(professores), 200)
        return paginate(Professor, cs)

    @jwt_required()
    def post(self):
        cs = professor_schema.ProfessorSchema()
        validate = cs.validate(request.json)
        if validate:
            return make_response(jsonify(validate), 400)
        else:
            nome = request.json["nome"]
            idade = request.json['idade']

            novo_professor = professor.Professor(nome=nome, idade=idade)
            resultado = professor_service.cadastrar_professor(novo_professor)
            x = cs.jsonify(resultado)
            return make_response(x, 201)


class ProfessorDetail(Resource):
    @jwt_required()
    def get(self, id):
        professor_id = professor_service.listar_professor_id(id)
        if professor_id is None:
            return make_response(jsonify('Professor não foi encontrado', 404))
        cs = professor_schema.ProfessorSchema()
        return make_response(cs.jsonify(professor_id), 200)

    @jwt_required()
    def put(self, id):
        professor_db = professor_service.listar_professor_id(id)
        if professor_db is None:
            return make_response(jsonify('Professor não foi encontrado', 404))
        cs = professor_schema.ProfessorSchema()
        validate = cs.validate(request.json)
        if validate:
            return make_response(jsonify(validate, 400))
        else:
            nome = request.json["nome"]
            idade = request.json['idade']
            novo_professor = professor.Professor(nome=nome, idade=idade)
            professor_service.atualiza_professor(professor_anterior=professor_db, professor_novo=novo_professor)
            professor_atualizado = professor_service.listar_professor_id(id)
            return make_response(cs.jsonify(professor_atualizado), 200)

    @jwt_required()
    def delete(self, id):
        professor_bd = professor_service.listar_professor_id(id)
        if professor_bd is None:
            return make_response(jsonify('Professor não encontrado', 404))
        professor_service.remove_professor(professor_bd)
        return make_response('Professor excluído com sucesso', 204)


api.add_resource(ProfessorList, '/professores')
api.add_resource(ProfessorDetail, '/professores/<int:id>')
