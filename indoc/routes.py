from indoc import app
from flask import render_template, redirect, flash, url_for, request
from indoc.forms import FormLogin, SolicitacaoCadastro, FormCriarConta

lista_clientes = ['Bruno Cesar', 'Luana Lorrane', 'Haline Melo']


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_solicitarcadastro = SolicitacaoCadastro()

    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        flash(f'Seja bem vindo {form_login.email.data}', 'alert-success')
        return redirect(url_for('home'))
    if form_solicitarcadastro.validate_on_submit() and 'botao_submit_enviar' in request.form:
        flash(f'Informações encaminhadas! Logo faremos parte do mesmo time.', 'alert-primary')

    return render_template('login.html', form_login=form_login, form_solicitarcadastro=form_solicitarcadastro)


@app.route("/perfil", methods=['GET', 'POST'])
def perfil():
    return render_template('perfil.html')


@app.route("/atendimento", methods=['GET', 'POST'])
def atendimento():
    return render_template('atendimentos.html')


@app.route("/usuario")
def usuario():
    form_cad_user = FormCriarConta()
    return render_template('usuarios.html', form_cad_user=form_cad_user)


@app.route("/cliente")
def cliente():
    return render_template('clientes.html', lista_clientes=lista_clientes)
