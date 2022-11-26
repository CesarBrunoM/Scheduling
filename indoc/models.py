from indoc import database, login_manager
from datetime import datetime
from flask_login import UserMixin, current_user


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
    ativo = database.Column(database.Boolean, default=True, nullable=False)
    data_cadastro = database.Column(database.DateTime, default=datetime.utcnow)
    logomarca = database.Column(database.String(150), default='default.jpg')
    usuario = database.relationship('Usuario', backref='empresa', lazy=True)
    cliente = database.relationship('Cliente', backref='empresa', lazy=True)
    setor = database.relationship('Setor', backref='empresa', lazy=True)
    problema = database.relationship('Problema', backref='empresa', lazy=True)
    atendimento = database.relationship('Atendimento', backref='empresa', lazy=True)


class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(100), nullable=False)
    nome_completo = database.Column(database.String(100), nullable=False)
    senha = database.Column(database.String(200), nullable=False)
    email = database.Column(database.String(100), nullable=False, unique=True)
    telefone = database.Column(database.String(12))
    foto_perfil = database.Column(database.String(150), default='default.jpg')
    data_nascimento = database.Column(database.DateTime, default=datetime.utcnow)
    data_cadastro = database.Column(database.DateTime, default=datetime.utcnow)
    cargo = database.Column(database.String(25), default='Não Informado')
    ativo = database.Column(database.Boolean, default=True, nullable=False)
    cad_user = database.Column(database.Boolean, default=True, nullable=False)
    cad_client = database.Column(database.Boolean, default=True, nullable=False)
    cad_setor = database.Column(database.Boolean, default=True, nullable=False)
    cad_problem = database.Column(database.Boolean, default=True, nullable=False)
    edit_user = database.Column(database.Boolean, default=True, nullable=False)
    edit_client = database.Column(database.Boolean, default=True, nullable=False)
    edit_setor = database.Column(database.Boolean, default=True, nullable=False)
    edit_problem = database.Column(database.Boolean, default=True, nullable=False)
    id_empresa = database.Column(database.Integer, database.ForeignKey('empresa.id'))
    atendimento = database.relationship('Atendimento', backref='usuario', lazy=True)
    atendente = database.relationship('SubAtendimento', backref='usuario', lazy=True)


class Cliente(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String(70))
    razao = database.Column(database.String(100))
    cnpj = database.Column(database.String(14))
    contato = database.Column(database.String(13))
    logomarca = database.Column(database.String(150), default='default.jpg')
    ativo = database.Column(database.Boolean, default=True, nullable=False)
    data_cadastro = database.Column(database.DateTime, default=datetime.utcnow)
    id_empresa = database.Column(database.Integer, database.ForeignKey('empresa.id'), nullable=False)
    participante = database.relationship('Atendimento', backref='cliente', lazy=True)


class Setor(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String(70))
    ativo = database.Column(database.Boolean, default=True, nullable=False)
    data_cadastro = database.Column(database.DateTime, default=datetime.utcnow)
    id_empresa = database.Column(database.Integer, database.ForeignKey('empresa.id'), nullable=False)
    atendimento = database.relationship('Atendimento', backref='setor', lazy=True)


class Problema(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    descricao = database.Column(database.String(200), nullable=False)
    ativo = database.Column(database.Boolean, default=True, nullable=False)
    data_cadastro = database.Column(database.DateTime, default=datetime.utcnow)
    id_empresa = database.Column(database.Integer, database.ForeignKey('empresa.id'), nullable=False)
    atendimento = database.relationship('Atendimento', backref='problema', lazy=True)
    subatendimento = database.relationship('SubAtendimento', backref='problema', lazy=True)


class Atendimento(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    protocolo = database.Column(database.Integer, nullable=False)
    data_cadastro = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    data_inicio = database.Column(database.DateTime)
    data_vencimento = database.Column(database.DateTime)
    data_conclusao = database.Column(database.DateTime)
    data_cancelamento = database.Column(database.DateTime)
    observacao = database.Column(database.String(300))
    obs_fechamento = database.Column(database.String(300))
    motivo_cancelamento = database.Column(database.String(200))
    prioridade = database.Column(database.String(20), nullable=False)
    solicitante = database.Column(database.String(35))
    tipo_atendimento = database.Column(database.String(10))
    status = database.Column(database.String(10), nullable=False, default='Aberto')
    id_empresa = database.Column(database.Integer, database.ForeignKey('empresa.id'), nullable=False)
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)
    id_problema = database.Column(database.Integer, database.ForeignKey('problema.id'), nullable=False)
    id_cliente = database.Column(database.Integer, database.ForeignKey('cliente.id'), nullable=False)
    id_setor = database.Column(database.Integer, database.ForeignKey('setor.id'), nullable=False)
    subatendimento = database.relationship('SubAtendimento', backref='atendimento', lazy=True)
    

class SubAtendimento(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    observacao = database.Column(database.String(300))
    data_cadastro = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    id_problema = database.Column(database.Integer, database.ForeignKey('problema.id'), nullable=False)
    id_atendimento = database.Column(database.Integer, database.ForeignKey('atendimento.id'), nullable=False)
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)

    