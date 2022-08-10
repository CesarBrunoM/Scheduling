from flask import Flask, render_template, url_for

app = Flask(__name__)

lista_clientes = ['Bruno Cesar', 'Luana Lorrane', 'Haline Melo']


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/login")
def login():
    return render_template('login.html')


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
