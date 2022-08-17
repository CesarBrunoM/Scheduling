from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp


class FormCriarConta():
    usuario = SubmitField('Nome usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email(message='Endereço de email invalido!')])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(8, 20)])
    confirma_senha = SubmitField('Confirmação senha', DataRequired(), EqualTo('senha'))
    botao_submit_criar = SubmitField('Concluir')


class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email(message='Endereço de email invalido!')])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    lembra_acesso = BooleanField('Lembrar acesso')
    botao_submit_login = SubmitField('Entrar')


class SolicitacaoCadastro(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message='Endereço de email invalido!')])
    whatsapp = StringField('Whatsapp',
                           validators=[DataRequired(),
                                       Length(11, 11)])
    botao_submit_enviar = SubmitField('Enviar')
