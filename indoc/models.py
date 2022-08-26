from indoc import database
from datetime import datetime


class UsuarioLogin(database.Model):
    id_user = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(25), nullable=False)
    nome_completo = database.Column(database.String(100), nullable=False)
    senha = database.Column(database.String(20), nullable=False)
    email = database.Column(database.String(100), nullable=False, unique=True)
    numerocontato = database.Column(database.String(12))
    foto_perfil = database.Column(database.String(150), default='default.jpg')
    data_nascimento = database.Column(database.DateTime)
    data_criacao = database.Column(database.DateTime, default=datetime.utcnow)
    id_profissao = database.Column(database.Integer, database.ForeignKey('profissao.id_profissao'), nullable=False)


class Profissao(database.Model):
    id_profissao = database.Column(database.Integer, primary_key=True)
    profissao_nome = database.Column(database.String(25), nullable=False)
    usuario = database.relationship('UsuarioLogin', backref='profissao', lazy=True)
