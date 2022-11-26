from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import SubmitField, StringField, PasswordField, BooleanField, SelectField, TextAreaField, DateTimeLocalField, \
    DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from indoc.models import Usuario, Cliente, Empresa
from flask_login import current_user
from datetime import datetime


class FormEmpresa(FlaskForm):
    nome = StringField('Nome empresa', validators=[DataRequired(), Length(1, 100)])
    razao = StringField('Razão social', validators=[DataRequired(), Length(1, 100)])
    cnpj = StringField('CNPJ', validators=[DataRequired(), Length(14, 14)])
    email = StringField('E-mail', validators=[DataRequired(), Email(message='Endereço de email invalido!')])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(8, 20)])
    confirma_senha = PasswordField('Confirmação senha', validators=[DataRequired(), EqualTo('senha',
                                                                                            message='Os campos de senha devem ser iguais.')])
    telefone = StringField('Nº Celular', validators=[DataRequired(), Length(11, 11)])
    logomarca = FileField('Logomarca', validators=[
    FileAllowed(['jpg', 'png', 'jpeg'], message='Arquivo invalido, selecione arquivos .jpg ou .png.')])
    botao_submit_concluir = SubmitField('Confirmar')

    def validate_cnpj(self, cnpj):
        empresa = Empresa.query.filter_by(cnpj=cnpj.data).first()
        if empresa:
            raise ValidationError('Empresa já cadastrada.')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('Email já cadastrado.')


class FormEditarEmpresa(FlaskForm):
    nome = StringField('Nome empresa', validators=[DataRequired(), Length(1, 100)])
    razao = StringField('Razão social', validators=[DataRequired(), Length(1, 100)])
    email = StringField('E-mail', validators=[DataRequired(), Email(message='Endereço de email invalido!')])
    telefone = StringField('Nº Celular', validators=[DataRequired(), Length(11, 11)])
    logomarca = FileField('Logomarca', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], message='Arquivo invalido, selecione arquivos .jpg ou .png.')])
    botao_submit_concluir = SubmitField('Confirmar')
            

class FormCriarConta(FlaskForm):
    username = StringField('Nome usuário', validators=[DataRequired(), Length(1, 100)])
    nome_completo = StringField('Nome completo', validators=[DataRequired(), Length(1, 100)])
    email = StringField('E-mail', validators=[DataRequired(), Email(message='Endereço de email invalido!')])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(8, 20)])
    confirma_senha = PasswordField('Confirmação senha', validators=[DataRequired(), EqualTo('senha',
                                                                                            message='Os campos de senha devem ser iguais.')])
    telefone = StringField('Nº Celular', validators=[DataRequired(), Length(11, 11)])
    foto_perfil = FileField('Foto perfil', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], message='Arquivo invalido, selecione arquivos .jpg ou .png.')])
    data_nascimento = DateField('Data Nascimento', default=datetime.today)
    cargo = StringField('Cargo', validators=[Length(1, 25)])
    ativo = BooleanField('Usuário ativo')
    cad_user = BooleanField('Cadastrar usuários')
    cad_client = BooleanField('Cadastrar clientes')
    cad_setor = BooleanField('Cadastrar setores')
    cad_problem = BooleanField('Cadastrar problemas')
    edit_user = BooleanField('Editar usuários')
    edit_client = BooleanField('Editar clientes')
    edit_setor = BooleanField('Editar setores')
    edit_problem = BooleanField('Editar problemas')
    edit_empresa = BooleanField('Editar Empresa')
    botao_submit_criar = SubmitField('Confirmar')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('Email já cadastrado.')


class FormLogin(FlaskForm):
    email = StringField('Usuário', validators=[DataRequired(), Email(message='Endereço de email invalido!')])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    lembra_acesso = BooleanField('Lembrar acesso')
    botao_submit_login = SubmitField('Entrar')


class FormEditarPerfil(FlaskForm):
    username = StringField('Nome usuário', validators=[DataRequired()])
    nome_completo = StringField('Nome completo', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email(message='Endereço de email invalido!')])
    senha = PasswordField('Senha')
    confirma_senha = PasswordField('Confirmação senha', validators=[EqualTo('senha' ,message='Os campos de senha devem ser iguais.')])
    telefone = StringField('Nº Celular', validators=[DataRequired(), Length(11, 11)])
    foto_perfil = FileField('Foto perfil', validators=[FileAllowed(['jpg', 'png', 'jpeg'], message='Arquivo invalido, selecione arquivos .jpg ou .png.')])
    data_nascimento = DateField('Data Nascimento', default=datetime.today)
    cargo = StringField('Cargo')
    botao_submit_editarperfil = SubmitField('Confirmar')
            
    def validate_senha(self, senha):
        if senha.data:
            if len(senha.data) < 8 or len(senha.data) > 20:
                raise ValidationError('Senha deve ter de 8 a 20 caracteres.')
    
    def validate_email(self, email):
        user = Usuario.query.filter_by(email=email.data).first()
        if user and user.id != current_user.id:
            raise ValidationError('E-mail já cadastrado.')


class FormEditarUsuario(FlaskForm):
    username = StringField('Nome usuário', validators=[DataRequired()])
    nome_completo = StringField('Nome completo', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email(message='Endereço de email invalido!')])
    senha = PasswordField('Senha')
    confirma_senha = PasswordField('Confirmação senha', validators=[EqualTo('senha',
                                                                            message='Os campos de senha devem ser iguais.')])
    telefone = StringField('Nº Celular', validators=[DataRequired(), Length(11, 11)])
    foto_perfil = FileField('Foto perfil', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], message='Arquivo invalido, selecione arquivos .jpg ou .png.')])
    data_nascimento = DateField('Data Nascimento', default=datetime.today)
    cargo = StringField('Cargo')
    ativo = BooleanField('Usuário ativo')
    cad_user = BooleanField('Cadastrar usuários')
    cad_client = BooleanField('Cadastrar clientes')
    cad_setor = BooleanField('Cadastrar setores')
    cad_problem = BooleanField('Cadastrar problemas')
    edit_user = BooleanField('Editar usuários')
    edit_client = BooleanField('Editar clientes')
    edit_setor = BooleanField('Editar setores')
    edit_problem = BooleanField('Editar problemas')
    edit_empresa = BooleanField('Editar Empresa')
    botao_submit_editarperfil = SubmitField('Confirmar')
        
    def validate_senha(self, senha):
        if senha.data:
            if len(senha.data) < 8 or len(senha.data) > 20:
                raise ValidationError('Senha deve ter de 8 a 20 caracteres.')


class FormCliente(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    razao = StringField('Razão social', validators=[DataRequired()])
    cnpj = StringField('CNPJ', validators=[DataRequired()])
    contato = StringField('Contato', validators=[DataRequired()])
    logomarca = FileField('Logomarca', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], message='Arquivo invalido, selecione arquivos .jpg ou .png.')])
    ativo = BooleanField('Ativo')
    btn_submit_cliente = SubmitField('Confirmar')  

    def validate_cnpj(self, cnpj):
        empresa = Cliente.query.filter_by(cnpj=cnpj.data, id_empresa=current_user.id_empresa).first()
        if empresa:
            raise ValidationError('Empresa já cadastrada.')
        
        
class FormEditarCliente(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    razao = StringField('Razão social', validators=[DataRequired()])
    cnpj = StringField('CNPJ', validators=[DataRequired()])
    contato = StringField('Contato', validators=[DataRequired()])
    logomarca = FileField('Logomarca', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], message='Arquivo invalido, selecione arquivos .jpg ou .png.')])
    ativo = BooleanField('Ativo')
    btn_submit_cliente = SubmitField('Confirmar')  
       

class FormProblema(FlaskForm):
    descricao = StringField('Descricao', validators=[DataRequired()])
    ativo = BooleanField('Ativo')
    btn_submit_problema = SubmitField('Confirmar')


class FormSetor(FlaskForm):
    nome = StringField('Nome setor', validators=[DataRequired()])
    ativo = BooleanField('Ativo')
    btn_submit_setor = SubmitField('Confirmar')


class FormAtendimento(FlaskForm):
    cliente = SelectField('Cliente', choices=[], coerce=int, validators=[DataRequired()])
    solicitante = StringField('Solicitante', validators=[DataRequired()])
    prioridade = SelectField('Prioridade', choices=[('Baixa'), ('Normal'), ('Alta'), ('Urgente')],
                             validators=[DataRequired()])
    problema = SelectField('Problema', choices=[], coerce=int, validators=[DataRequired()])
    data_vencimento = DateTimeLocalField('Data Vencimento', default=datetime.today, format='%Y-%m-%dT%H:%M')
    setor = SelectField('Setor', choices=[], coerce=int, validators=[DataRequired()])
    observacao = TextAreaField('Observação', validators=[DataRequired()])
    btn_submit_novo = SubmitField('Confirmar')

    def validate_choices(self):
        if len(self.cliente.choices == 0):
            return False
        return True


class FormComentario(FlaskForm):
    usuario = SelectField('Usuário', choices=[], coerce=int, validators=[DataRequired()])
    problema = SelectField('Problema', choices=[], coerce=int, validators=[DataRequired()])
    observacao = TextAreaField('Observação', validators=[DataRequired()])
    btn_submit_salvar = SubmitField('Salvar')


class FormCancelamento(FlaskForm):
    motivo = TextAreaField('Motivo cancelamento', validators=[DataRequired()])
    btn_submit_cancelar = SubmitField('Concluir')


class FormFecharAtendimento(FlaskForm):
    obs_fechamento = TextAreaField('Solução', validators=[DataRequired()])
    btn_submit_fechar = SubmitField('Concluir')
