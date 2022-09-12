from indoc import app, bcrypt
from flask import render_template, redirect, flash, url_for, request
from indoc.forms import FormLogin, SolicitacaoCadastro, FormCriarConta
from indoc.models import Usuario, database
from flask_login import login_user

lista_clientes = ['Bruno Cesar', 'Luana Lorrane', 'Haline Melo']


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_solicitarcadastro = SolicitacaoCadastro()

    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        user = Usuario.query.filter_by(email=form_login.email.data).first()
        if user and bcrypt.check_password_hash(user.senha, form_login.senha.data):
            login_user(user, remember=form_login.lembra_acesso.data)
            flash(f'Seja bem vindo {user.username}', 'alert-success')
            return redirect(url_for('home'))
        else:
            flash('Falha no login, verifique seu email e senha.', 'alert-danger')
    if form_solicitarcadastro.validate_on_submit() and 'botao_submit_enviar' in request.form:
        flash(f'Informações encaminhadas! Logo faremos parte do mesmo time.', 'alert-primary')

    return render_template('login.html', form_login=form_login, form_solicitarcadastro=form_solicitarcadastro)


@app.route("/perfil", methods=['GET', 'POST'])
def perfil():
    return render_template('perfil.html')


@app.route("/atendimento", methods=['GET', 'POST'])
def atendimento():
    return render_template('atendimentos.html')


@app.route("/usuarios", methods=['GET', 'POST'])
def usuario():
    form_criarconta = FormCriarConta()
    if form_criarconta.validate_on_submit() and 'botao_submit_criar' in request.form:
        senha_cript = bcrypt.generate_password_hash(form_criarconta.senha.data)
        usuario = Usuario(username=form_criarconta.username.data,
                          nome_completo=form_criarconta.nome_completo.data,
                          email=form_criarconta.email.data,
                          telefone=form_criarconta.telefone.data,
                          senha=senha_cript,
                          cargo=form_criarconta.cargo.data)
        database.session.add(usuario)
        database.session.commit()
        redirect(url_for('home'))
        flash(f'Usuário {form_criarconta.username.data} cadastrado com sucesso', 'alert-success')
    return render_template('usuarios.html', form_criarconta=form_criarconta)


@app.route("/cliente")
def cliente():
    return render_template('clientes.html', lista_clientes=lista_clientes)
