from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import SubmitField, StringField, PasswordField, BooleanField, DateField, FieldList, IntegerField
from wtforms.fields import TelField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from indoc.models import Usuario, Clienteempresa
from flask_login import current_user


class FormEmpresa(FlaskForm):
    nome = StringField('Nome empresa', validators=[DataRequired()])
    razao = StringField('Razão social', validators=[DataRequired()])
    cnpj = StringField('CNPJ', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email(message='Endereço de email invalido!')])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(8, 20)])
    confirma_senha = PasswordField('Confirmação senha', validators=[DataRequired(), EqualTo('senha',
                                                                                            message='Os campos de senha devem ser iguais.')])
    telefone = TelField('Nº Celular', validators=[DataRequired(), Length(11, 11)])
    botao_submit_concluir = SubmitField('Confirmar')


class FormCriarConta(FlaskForm):
    username = StringField('Nome usuário', validators=[DataRequired()])
    nome_completo = StringField('Nome completo', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email(message='Endereço de email invalido!')])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(8, 20)])
    confirma_senha = PasswordField('Confirmação senha', validators=[DataRequired(), EqualTo('senha',
                                                                                            message='Os campos de senha devem ser iguais.')])
    telefone = TelField('Nº Celular', validators=[DataRequired(), Length(11, 11)])
    foto_perfil = FileField('Foto perfil', validators=[
        FileAllowed(['jpg', 'png'], message='Arquivo invalido, selecione arquivos .jpg ou .png.')])
    data_nascimento = DateField('Data Nascimento', validators=[DataRequired()])
    cargo = StringField('Cargo')
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


class SolicitacaoCadastro(FlaskForm):
    emailrequerido = StringField('Email', validators=[DataRequired(), Email(message='Endereço de email invalido!')])
    whatsapp = StringField('Whatsapp',
                           validators=[DataRequired(),
                                       Length(11, 11)])
    botao_submit_enviar = SubmitField('Enviar')


class FormEditarPerfil(FlaskForm):
    username = StringField('Nome usuário', validators=[DataRequired()])
    nome_completo = StringField('Nome completo', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email(message='Endereço de email invalido!')])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(8, 20)])
    confirma_senha = PasswordField('Confirmação senha', validators=[DataRequired(), EqualTo('senha',
                                                                                            message='Os campos de senha devem ser iguais.')])
    telefone = TelField('Nº Celular', validators=[DataRequired(), Length(11, 11)])
    foto_perfil = FileField('Foto perfil', validators=[
        FileAllowed(['jpg', 'png'], message='Arquivo invalido, selecione arquivos .jpg ou .png.')])
    data_nascimento = DateField('Data Nascimento', validators=[DataRequired()])
    cargo = StringField('Cargo')
    botao_submit_editarperfil = SubmitField('Confirmar')

    def validate_email(self, email):
        if current_user.email != email.data:
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError('Já existe um usuário com este email, utilize outro email para continuar.')


class EmpresaCliente(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    razao = StringField('Razão social', validators=[DataRequired()])
    cnpj = StringField('CNPJ', validators=[DataRequired()])
    btn_submit_cadempresa = SubmitField('Confirmar')

    def validate_cnpj(self, cnpj):
        empresa = Clienteempresa.query.filter_by(cnpj=cnpj.data, id_empresa=current_user.id_empresa).first()
        if empresa:
            raise ValidationError('Empresa já cadastrada.')


class FormCliente(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    contato = TelField('Contato', validators=[DataRequired()])
    id_cli_empresa = StringField('Empresa')
    btn_submit_cliente = SubmitField('Confirmar')


class FormProblema(FlaskForm):
    descricao = StringField('Descricao', validators=[DataRequired()])


class FormSetor(FlaskForm):
    nome = StringField('Nome setor', validators=[DataRequired()])
