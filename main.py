from flask import Flask, render_template, url_for
from forms import FormLogin, SolicitacaoCadastro

app = Flask(__name__)

lista_clientes = ['Bruno Cesar', 'Luana Lorrane', 'Haline Melo']

app.config['SECRET_KEY'] = '6025524ac8f6491f7d860090f8e77a47'

@app.route("/")
def home():
    return render_template('home.html')


@app.route("/login")
def login():
    form_login = FormLogin()
    form_solicitarcadastro = SolicitacaoCadastro()
    return render_template('login.html', form_login=form_login, form_solicitarcadastro=form_solicitarcadastro)


@app.route("/perfil")
def perfil():
    return render_template('perfil.html')


@app.route("/atendimento")
def atendimento():
    return render_template('atendimentos.html')


@app.route("/usuario")
def usuario():
    return render_template('usuarios.html')


@app.route("/cliente")
def cliente():
    return render_template('clientes.html', lista_clientes=lista_clientes)


if __name__ == '__main__':
    app.run(debug=True)
