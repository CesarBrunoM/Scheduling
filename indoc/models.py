from indoc import database, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_usuario(id_user):
    return Usuario.query.get(int(id_user))


class Empresa(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    cnpj = database.Column(database.String(14), unique=True)
    razao = database.Column(database.String(100))
    nome = database.Column(database.String(100))
    email = database.Column(database.String(100), nullable=False, unique=True)
    telefone = database.Column(database.String(12))
    usuario = database.relationship('Usuario', backref='empresa', lazy=True)
    cliente = database.relationship('Cliente', backref='empresa', lazy=True)
    setor = database.relationship('Setor', backref='empresa', lazy=True)
    problema = database.relationship('Problema', backref='empresa', lazy=True)
    atendimento = database.relationship('Atendimento', backref='empresa', lazy=True)


class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(25), nullable=False)
    nome_completo = database.Column(database.String(100), nullable=False)
    senha = database.Column(database.String(200), nullable=False)
    email = database.Column(database.String(100), nullable=False, unique=True)
    telefone = database.Column(database.String(12))
    foto_perfil = database.Column(database.String(150), default='default.jpg')
    data_nascimento = database.Column(database.DateTime)
    data_criacao = database.Column(database.DateTime, default=datetime.utcnow)
    cargo = database.Column(database.String(25), default='Não Informado')
    id_empresa = database.Column(database.Integer, database.ForeignKey('empresa.id'))
    atendimento = database.relationship('ParticipanteUsuario', backref='usuario', lazy=True)


class Cliente(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String(70))
    razao = database.Column(database.String(100))
    cnpj = database.Column(database.String(14))
    contato = database.Column(database.String(13))
    id_empresa = database.Column(database.Integer, database.ForeignKey('empresa.id'), nullable=False)
    participante = database.relationship('Atendimento', backref='cliente', lazy=True)


class Setor(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String(70))
    id_empresa = database.Column(database.Integer, database.ForeignKey('empresa.id'), nullable=False)
    atendimento = database.relationship('Atendimento', backref='setor', lazy=True)


class Problema(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    descricao = database.Column(database.String(200), nullable=True)
    id_empresa = database.Column(database.Integer, database.ForeignKey('empresa.id'), nullable=False)
    atendimento = database.relationship('Atendimento', backref='problema', lazy=True)


class Atendimento(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    protocolo = database.Column(database.String(20), nullable=False)
    data_cadastro = database.Column(database.DateTime, nullable=False)
    data_inicio = database.Column(database.DateTime, nullable=False)
    data_vencimento = database.Column(database.DateTime, nullable=False)
    local = database.Column(database.String(20), nullable=False)
    observacao = database.Column(database.String(300))
    id_empresa = database.Column(database.Integer, database.ForeignKey('empresa.id'), nullable=False)
    id_prioridade = database.Column(database.Integer, database.ForeignKey('prioridade.id'), nullable=False)
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)
    id_problema = database.Column(database.Integer, database.ForeignKey('problema.id'), nullable=False)
    id_cliente = database.Column(database.Integer, database.ForeignKey('cliente.id'), nullable=False)
    id_setor = database.Column(database.Integer, database.ForeignKey('setor.id'), nullable=False)
    participante = database.relationship('ParticipanteUsuario', backref='atendimento', lazy=True)


class Prioridade(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    descricao = database.Column(database.String(20), nullable=False)
    cor = database.Column(database.String(20), nullable=False)
    atendimento = database.relationship('Atendimento', backref='prioridade', lazy=True)


class ParticipanteUsuario(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)
    id_atendimento = database.Column(database.Integer, database.ForeignKey('atendimento.id'), nullable=False)
