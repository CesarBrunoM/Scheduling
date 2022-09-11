from indoc import database
from datetime import datetime


class Usuario(database.Model):
    id_user = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(25), nullable=False)
    nome_completo = database.Column(database.String(100), nullable=False)
    senha = database.Column(database.String(200), nullable=False)
    email = database.Column(database.String(100), nullable=False, unique=True)
    telefone = database.Column(database.String(12))
    foto_perfil = database.Column(database.String(150), default='default.jpg')
    data_nascimento = database.Column(database.DateTime)
    data_criacao = database.Column(database.DateTime, default=datetime.utcnow)
    cargo = database.Column(database.String(25), default='Não Informado')


class Cliente(database.Model):
    id_cliente = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String(70))
    contato = database.Column(database.String(13))
    id_empresa = database.Column(database.Integer, database.ForeignKey('clienteempresa.id_empresa'))
    atendimento = database.relationship('Cliente', backref='atendimentos', lazy=True)
    # id_profissao = database.Column(database.Integer, database.ForeignKey('profissao.id_profissao'), nullable=False)
    # usuario = database.relationship('UsuarioLogin', backref='profissao', lazy=True)


class Clienteempresa(database.Model):
    id_empresa = database.Column(database.Integer, primary_key=True)
    razao = database.Column(database.String(100))
    nome = database.Column(database.String(100))
    cliente = database.relationship('Cliente', backref='clienteempresa', lazy=True)


class Setor(database.Model):
    id_setor = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String(70))
    atendimento = database.relationship('Atendimentos', backref='setor', lazy=True)


class Problemas(database.Model):
    id_problema = database.Column(database.Integer, primary_key=True)
    descricao = database.Column(database.String(200), nullable=True)
    atendimentos = database.relationship('Atendimentos', backref='problemas', lazy=True)


class Atendimentos(database.Model):
    id_atendimento = database.Column(database.Integer, primary_key=True)
    protocolo = database.Column(database.String(20), nullable=False)
    data_cadastro = database.Column(database.DateTime, nullable=False)
    data_inicio = database.Column(database.DateTime, nullable=False)
    data_vencimento = database.Column(database.DateTime, nullable=False)
    prioridade = database.Column(database.String(20), nullable=False)
    local = database.Column(database.String(20), nullable=False)
    observacao = database.Column(database.String(300))
    problema = database.Column(database.String(200), nullable=False)
    id_cliente = database.Column(database.Integer, database.ForeignKey('cliente.id_cliente'), nullable=False)
    id_setor = database.Column(database.Integer, database.ForeignKey('setor.id_setor'), nullable=False)