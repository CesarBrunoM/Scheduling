from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from indoc.models import Usuario

class FormCriarConta(FlaskForm):
    username = StringField('Nome usuário', validators=[DataRequired()])
    nome_completo = StringField('Nome completo', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email(message='Endereço de email invalido!')])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(8, 20)])
    confirma_senha = PasswordField('Confirmação senha', validators=[DataRequired(), EqualTo('senha')])
    telefone = StringField('Nº Celular', validators=[DataRequired(), Length(11, 11)])
    cargo = StringField('Cargo')
    botao_submit_criar = SubmitField('Gravar')

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
