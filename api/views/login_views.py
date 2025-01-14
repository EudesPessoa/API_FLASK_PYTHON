from flask_restful import Resource
from api import api, jwt
from ..schemas import login_schema
from flask import request, make_response, jsonify
from ..services import usuario_service
from flask_jwt_extended import create_access_token, create_refresh_token
from datetime import timedelta


class LoginList(Resource):

    @jwt.additional_claims_loader
    def add_claims_to_access_token(identify):
        usuario_token = usuario_service.listar_usuario_id(identify)
        if usuario_token.is_admin:
            roles = 'admin'
        else:
            roles = 'user'
        return {'roles':roles}


    def post(self):
        ls = login_schema.LoginSchema()
        validate = ls.validate(request.json)
        if validate:
            return make_response(jsonify(validate), 400)
        else:
            email = request.json['email']
            senha = request.json['senha']

            usuario_db = usuario_service.listar_usuario_email(email=email)

            if usuario_db and usuario_db.ver_senha(senha=senha):
                access_token = create_access_token(
                    identity=usuario_db.id,
                    expires_delta=timedelta(seconds=100)
                )
                refresh_token = create_refresh_token(
                    identity=usuario_db.id
                )
                return make_response(jsonify({
                    "access_token":access_token,
                    "refresh_token":refresh_token,
                    "message":"Login Realizado com sucesso"
                }), 200)

            return make_response(jsonify({
                "message":"Credenciais estão invalidas"
            }), 401)


api.add_resource(LoginList, '/login')
