from flask import Flask, render_template, url_for, request, flash, redirect
from forms import FormLogin, SolicitacaoCadastro, FormCriarConta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

lista_clientes = ['Bruno Cesar', 'Luana Lorrane', 'Haline Melo']

app.config['SECRET_KEY'] = '6025524ac8f6491f7d860090f8e77a47'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/systembd'

database = SQLAlchemy(app)

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


if __name__ == '__main__':
    app.run(debug=True)
