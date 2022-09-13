from indoc import app, bcrypt
from flask import render_template, redirect, flash, url_for, request
from indoc.forms import FormLogin, SolicitacaoCadastro, FormCriarConta
from indoc.models import Usuario, database
from flask_login import login_user, logout_user, current_user, login_required

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
            par_next = request.args.get('next')
            if par_next:
                return redirect(par_next)
            else:
                return redirect(url_for('home'))
        else:
            flash('Falha no login, verifique seu email e senha.', 'alert-danger')
    if form_solicitarcadastro.validate_on_submit() and 'botao_submit_enviar' in request.form:
        flash(f'Informações encaminhadas! Logo faremos parte do mesmo time.', 'alert-primary')

    return render_template('login.html', form_login=form_login, form_solicitarcadastro=form_solicitarcadastro)


@app.route("/perfil/", methods=['GET', 'POST'])
@login_required
def perfil():
    return render_template('perfil.html')


@app.route("/atendimento", methods=['GET', 'POST'])
@login_required
def atendimento():
    return render_template('atendimentos.html')


@app.route("/usuario", methods=['GET', 'POST'])
@login_required
def usuario():
    form_criarconta = FormCriarConta()
    if form_criarconta.validate_on_submit() and 'botao_submit_criar' in request.form:
        senha_cript = bcrypt.generate_password_hash(form_criarconta.senha.data)
        user = Usuario(username=form_criarconta.username.data,
                       nome_completo=form_criarconta.nome_completo.data,
                       email=form_criarconta.email.data,
                       telefone=form_criarconta.telefone.data,
                       senha=senha_cript,
                       cargo=form_criarconta.cargo.data)
        database.session.add(user)
        database.session.commit()
        redirect(url_for('home'))
        flash(f'Usuário {form_criarconta.username.data} cadastrado com sucesso', 'alert-success')
    return render_template('usuarios.html', form_criarconta=form_criarconta)


@app.route("/cliente")
@login_required
def cliente():
    return render_template('clientes.html', lista_clientes=lista_clientes)


@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash('Sua sessão foi encerrada.', 'alert-success')
    return redirect('login')
