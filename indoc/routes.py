from indoc import app, bcrypt
from flask import render_template, redirect, flash, url_for, request
from indoc.forms import FormLogin, SolicitacaoCadastro, FormCriarConta, FormEditarPerfil, FormEmpresa, EmpresaCliente, \
    FormCliente
from indoc.models import Usuario, database, Empresa, Clienteempresa, Cliente
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image


@app.route("/")
def home():
    return render_template('home.html')


def salvar_imagem(imagem):
    codigo = secrets.token_hex(8)
    nome, extencao = os.path.splitext(imagem.filename)
    nome_arquivo = nome + '_' + codigo + extencao
    caminho_imagem = os.path.join(app.root_path, 'static/foto_perfil', nome_arquivo)

    tamanho = (200, 200)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    imagem_reduzida.save(caminho_imagem)
    return nome_arquivo


@app.route("/empresa/cadastro", methods=['GET', 'POST'])
def empresacadastro():
    formempresa = FormEmpresa()
    if formempresa.validate_on_submit() and 'botao_submit_concluir' in request.form:
        cript_senha = bcrypt.generate_password_hash(formempresa.senha.data)
        empresa = Empresa(razao=formempresa.razao.data,
                          nome=formempresa.nome.data,
                          cnpj=formempresa.cnpj.data,
                          email=formempresa.email.data,
                          telefone=formempresa.telefone.data)
        database.session.add(empresa)
        database.session.commit()

        id_empresa = Empresa.query.filter_by(cnpj=formempresa.cnpj.data).first()
        useradm = Usuario(username=formempresa.nome.data,
                          nome_completo=formempresa.razao.data,
                          email=formempresa.email.data,
                          telefone=formempresa.telefone.data,
                          senha=cript_senha,
                          cargo='Master',
                          id_empresa=id_empresa.id)
        database.session.add(useradm)
        database.session.commit()

        user = Usuario.query.filter_by(email=formempresa.email.data).first()
        if user and bcrypt.check_password_hash(user.senha, formempresa.senha.data):
            login_user(user)
            flash(f'Seja bem vindo {user.username}', 'alert-success')
        else:
            flash('Falha no login, verifique seu email e senha.', 'alert-danger')
        return redirect(url_for('home'))

    return render_template('cadastro_empresa.html', formempresa=formempresa)


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


@app.route("/usuario/cadastro", methods=['GET', 'POST'])
# @login_required
def usuario():
    form_criarconta = FormCriarConta()
    if form_criarconta.validate_on_submit() and 'botao_submit_criar' in request.form:
        senha_cript = bcrypt.generate_password_hash(form_criarconta.senha.data)
        if form_criarconta.foto_perfil.data:
            nome_imagem = salvar_imagem(form_criarconta.foto_perfil.data)
            user = Usuario(username=form_criarconta.username.data,
                           nome_completo=form_criarconta.nome_completo.data,
                           email=form_criarconta.email.data,
                           telefone=form_criarconta.telefone.data,
                           data_nascimento=form_criarconta.data_nascimento.data,
                           senha=senha_cript,
                           cargo=form_criarconta.cargo.data,
                           id_empresa=current_user.id_empresa,
                           foto_perfil=nome_imagem)
        else:
            user = Usuario(username=form_criarconta.username.data,
                           nome_completo=form_criarconta.nome_completo.data,
                           email=form_criarconta.email.data,
                           telefone=form_criarconta.telefone.data,
                           data_nascimento=form_criarconta.data_nascimento.data,
                           senha=senha_cript,
                           cargo=form_criarconta.cargo.data,
                           id_empresa=current_user.id_empresa)
        database.session.add(user)
        database.session.commit()
        flash(f'Usuário {form_criarconta.username.data} cadastrado com sucesso', 'alert-success')
        return redirect(url_for('home'))
    return render_template('usuarios.html', form_criarconta=form_criarconta)


@app.route("/perfil", methods=['GET', 'POST'])
@login_required
def perfil():
    foto_perfil = url_for('static', filename='foto_perfil/{}'.format(current_user.foto_perfil))
    return render_template('perfil.html', foto_perfil=foto_perfil)


@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editarperfil():
    form = FormEditarPerfil()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.nome_completo = form.nome_completo.data
        current_user.email = form.email.data
        current_user.telefone = form.telefone.data
        current_user.data_nascimento = form.data_nascimento.data
        current_user.cargo = form.cargo.data
        if form.foto_perfil.data:
            nome_imagem = salvar_imagem(form.foto_perfil.data)
            current_user.foto_perfil = nome_imagem
        database.session.commit()
        flash('Perfil atualizado com sucesso', 'alert-success')
        return redirect(url_for('perfil'))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.nome_completo.data = current_user.nome_completo
        form.email.data = current_user.email
        form.telefone.data = current_user.telefone
        form.data_nascimento.data = current_user.data_nascimento
        form.cargo.data = current_user.cargo
    foto_perfil = url_for('static', filename='foto_perfil/{}'.format(current_user.foto_perfil))
    return render_template('editarperfil.html', form_editar_perfil=form, foto_perfil=foto_perfil)


@app.route("/cliente/cadastro", methods=['GET', 'POST'])
@login_required
def cadastrocliente():
    form = FormCliente()
    if form.validate_on_submit() and 'btn_submit_cliente' in request.form:
        client = Cliente(
            nome=form.nome.data,
            contato=form.contato.data,
            id_cli_empresa=form.id_cli_empresa.data,
            id_empresa=current_user.id_empresa
        )
        database.session.add(client)
        database.session.commit()
        flash(f'Cliente {form.nome.data} cadastrado com sucesso.')
        return redirect(url_for('cliente'))
    return render_template('cadastro_cliente.html', form=form)


@app.route("/cliente")
@login_required
def cliente():
    lista_cliente = Cliente.query.filter_by(id_empresa=current_user.id_empresa)
    return render_template('clientes.html', lista_clientes=lista_cliente)


@app.route("/usuario")
@login_required
def listuser():
    lista_usuarios = Usuario.query.filter_by(id_empresa=current_user.id_empresa)
    return render_template('lista_usuarios.html', lista_usuarios=lista_usuarios)


@app.route("/atendimento", methods=['GET', 'POST'])
@login_required
def atendimento():
    return render_template('atendimentos.html')


@app.route("/empresas", methods=['GET', 'POST'])
@login_required
def lista_empresa():
    lista = Clienteempresa.query.filter_by(id_empresa=current_user.id_empresa)
    return render_template('empresas_cliente.html', lista=lista)


@app.route("/cliente/empresa/cadastro", methods=['GET', 'POST'])
@login_required
def empresacliente():
    form = EmpresaCliente()
    if form.validate_on_submit() and 'btn_submit_cadempresa' in request.form:
        cadempresa = Clienteempresa(
            razao=form.razao.data,
            nome=form.nome.data,
            cnpj=form.cnpj.data,
            id_empresa=current_user.id_empresa)
        database.session.add(cadempresa)
        database.session.commit()
        flash(f'Empresa {form.nome.data} cadastrada com sucesso.', 'alert-success')
        return redirect(url_for('lista_empresa'))

    return render_template('cliente_empresa_cad.html', form=form)


@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash('Sua sessão foi encerrada.', 'alert-success')
    return redirect('login')
