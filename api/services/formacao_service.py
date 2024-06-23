from ..models import formacao_model
from api import db
from .professor_service import listar_professor_id

def cadastrar_formacao(formacao):
    formacao_bd = formacao_model.Formacao(nome=formacao.nome, descricao=formacao.descricao)
    for i in formacao.professores:
        professor = listar_professor_id(i)
        if professor not in formacao_bd.professores:
            formacao_bd.professores.append(professor)

    db.session.add(formacao_bd)
    db.session.commit()
    return formacao_bd


def listar_formacoes():
    formacoes = formacao_model.Formacao.query.all()
    return formacoes


def listar_formacao_id(id):
    formacao = formacao_model.Formacao.query.filter_by(id=id).first()
    return formacao


def atualiza_formacao(formacao_anterior, formacao_nova):
    formacao_anterior.nome = formacao_nova.nome
    formacao_anterior.descricao = formacao_nova.descricao

    existing_professores = set((professor.id for professor in formacao_anterior.professores))

    for i in formacao_nova.professores:
        professor_id = i.get("id")
        if professor_id is not None and professor_id not in existing_professores:
            professor = listar_professor_id(professor_id)
            if professor:
                formacao_anterior.professores.append(professor)
    db.session.commit()


def remove_formacao(formacao):
    db.session.delete(formacao)
    db.session.commit()
