from indoc import app, bcrypt
from flask import render_template, redirect, flash, url_for, request
from indoc.forms import FormLogin, FormCriarConta, FormEditarPerfil, FormEmpresa, FormCliente, \
    FormProblema, FormSetor, FormEditarUsuario, FormAtendimento, FormComentario, FormCancelamento, FormFecharAtendimento, \
    FormEditarEmpresa
from indoc.models import Usuario, database, Empresa, Cliente, Problema, Setor, Atendimento, SubAtendimento
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image
from datetime import datetime


@app.route("/")
@login_required
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


def salvar_logomarca_cliente(imagem):
    codigo = secrets.token_hex(8)
    nome, extencao = os.path.splitext(imagem.filename)
    nome_arquivo = nome + '_' + codigo + extencao
    caminho_imagem = os.path.join(app.root_path, 'static/logomarca_cliente', nome_arquivo)

    tamanho = (200, 200)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    imagem_reduzida.save(caminho_imagem)
    return nome_arquivo


def salvar_logomarca_empresa(imagem):
    codigo = secrets.token_hex(8)
    nome, extencao = os.path.splitext(imagem.filename)
    nome_arquivo = nome + '_' + codigo + extencao
    caminho_imagem = os.path.join(app.root_path, 'static/logomarca_empresa', nome_arquivo)

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
        if formempresa.logomarca:
            logomarca = salvar_logomarca_empresa(formempresa.logomarca.data)        
            empresa = Empresa(razao=formempresa.razao.data,
                            nome=formempresa.nome.data,
                            cnpj=formempresa.cnpj.data,
                            email=formempresa.email.data,
                            telefone=formempresa.telefone.data,
                            logomarca=logomarca)
        else:
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


@app.route("/empresa/perfil", methods=['GET', 'POST'])
@login_required
def empresa():
    return render_template('perfil_empresa.html', datetime=datetime)


@app.route("/empresa_empresa/<id_empresa>", methods=['GET', 'POST'])
@login_required
def editarempresa(id_empresa):
    formempresa = FormEditarEmpresa()
    empresa = Empresa.query.get(id_empresa)
    if formempresa.validate_on_submit() and 'botao_submit_concluir' in request.form:
        empresa.cnpj=formempresa.cnpj.data
        empresa.razao=formempresa.razao.data
        empresa.nome=formempresa.nome.data
        empresa.email=formempresa.email.data
        empresa.telefone=formempresa.telefone.data
        if formempresa.logomarca.data:
            logomarca = salvar_logomarca_empresa(formempresa.logomarca.data)
            empresa.logomarca=logomarca
        database.session.commit()
        flash('Empresa atualizada com sucesso', 'alert-success')
        return redirect(url_for('empresa'))
    elif request.method == "GET":
        formempresa.cnpj.data=empresa.cnpj
        formempresa.nome.data=empresa.nome
        formempresa.razao.data=empresa.razao
        formempresa.email.data=empresa.email
        formempresa.telefone.data=empresa.telefone
    
    return render_template('editar_empresa.html', formempresa=formempresa, datetime=datetime)



@app.route("/login", methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
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

    return render_template('login.html', form_login=form_login)


@app.route("/usuario/cadastro", methods=['GET', 'POST'])
@login_required
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
        return redirect(url_for('listuser'))
    return render_template('usuarios.html', form_criarconta=form_criarconta)


@app.route("/perfil", methods=['GET'])
@login_required
def perfil():
    foto_perfil = url_for('static', filename='foto_perfil/{}'.format(current_user.foto_perfil))
    return render_template('perfil.html', foto_perfil=foto_perfil, datetime=datetime)


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
    return render_template('editarperfil.html', form_editar_perfil=form, foto_perfil=foto_perfil, datetime=datetime)


@app.route("/usuario")
@login_required
def listuser():
    foto_perfil = url_for('static', filename='foto_perfil/{}'.format(current_user.foto_perfil))
    lista_usuarios = Usuario.query.filter_by(id_empresa=current_user.id_empresa)
    return render_template('lista_usuarios.html', lista_usuarios=lista_usuarios, datetime=datetime, foto_perfil=foto_perfil)


@app.route("/usuario/<usuario_id>", methods=['GET', 'POST'])
@login_required
def editar_usuario(usuario_id):
    form = FormEditarUsuario()
    user = Usuario.query.get(usuario_id)
    if request.method == "GET":
        form.username.data = user.username
        form.nome_completo.data = user.nome_completo
        form.email.data = user.email
        form.telefone.data = user.telefone
        form.data_nascimento.data = user.data_nascimento
        form.cargo.data = user.cargo
        form.ativo.data = user.ativo
    elif form.validate_on_submit() and user.email != form.email.data:
        user.username = form.username.data
        user.nome_completo = form.nome_completo.data
        user.email = form.email.data
        user.telefone = form.telefone.data
        user.data_nascimento = form.data_nascimento.data
        user.cargo = form.cargo.data
        user.ativo = form.ativo.data
        if form.foto_perfil.data:
            nome_imagem = salvar_imagem(form.foto_perfil.data)
            user.foto_perfil = nome_imagem
        database.session.commit()
        flash(f'Usuário {form.username.data} atualizado com sucesso', 'alert-success')
        return redirect(url_for('listuser'))
    else:
        user.username = form.username.data
        user.nome_completo = form.nome_completo.data
        user.telefone = form.telefone.data
        user.data_nascimento = form.data_nascimento.data
        user.cargo = form.cargo.data
        user.ativo = form.ativo.data
        if form.foto_perfil.data:
            nome_imagem = salvar_imagem(form.foto_perfil.data)
            user.foto_perfil = nome_imagem
        database.session.commit()
        flash(f'Usuário {form.username.data} atualizado com sucesso', 'alert-success')
        return redirect(url_for('listuser'))

    foto_perfil = url_for('static', filename='foto_perfil/{}'.format(user.foto_perfil))
    return render_template('editar_usuario.html', form=form, foto_perfil=foto_perfil, usuario=user)


@app.route("/cliente/cadastro", methods=['GET', 'POST'])
@login_required
def cadastrocliente():
    form = FormCliente()
    if form.validate_on_submit() and 'btn_submit_cliente' in request.form:
        if form.logomarca.data:
            logomarca = salvar_logomarca_cliente(form.logomarca.data)
            client = Cliente(
                nome=form.nome.data,
                razao=form.razao.data,
                cnpj=form.cnpj.data,
                contato=form.contato.data,
                ativo=form.ativo.data,
                logomarca=logomarca,
                id_empresa=current_user.id_empresa)
        else:
            client = Cliente(
                nome=form.nome.data,
                razao=form.razao.data,
                cnpj=form.cnpj.data,
                contato=form.contato.data,
                ativo=form.ativo.data,
                id_empresa=current_user.id_empresa)
        database.session.add(client)
        database.session.commit()
        flash(f'Cliente {form.nome.data} cadastrado com sucesso.', 'alert-success')
        return redirect(url_for('cliente'))
    return render_template('cadastro_cliente.html', form=form)


@app.route("/cliente")
@login_required
def cliente():
    lista_cliente = Cliente.query.filter_by(id_empresa=current_user.id_empresa)
    return render_template('clientes.html', lista_clientes=lista_cliente)


@app.route("/cliente/<cliente_id>", methods=['GET', 'POST'])
@login_required
def editar_cliente(cliente_id):
    form = FormCliente()
    client = Cliente.query.get(cliente_id)
    if request.method == 'GET':
        form.nome.data = client.nome
        form.razao.data = client.razao
        form.cnpj.data = client.cnpj
        form.contato.data = client.contato
        form.ativo.data = client.ativo
    elif form.validate_on_submit() and client.cnpj != form.cnpj.data:
        client.nome = form.nome.data
        client.razao = form.razao.data
        client.contato = form.contato.data
        client.ativo = form.ativo.data
        if form.logomarca.data:
            nome_imagem = salvar_logomarca_cliente(form.logomarca.data)
            client.logomarca = nome_imagem
        database.session.commit()
        flash(f'client {form.nome.data} atualizado com sucesso.')
        return redirect(url_for('cliente'))
    else:
        client.nome = form.nome.data
        client.razao = form.razao.data
        client.contato = form.contato.data
        client.ativo = form.ativo.data
        if form.logomarca.data:
            nome_imagem = salvar_logomarca_cliente(form.logomarca.data)
            client.logomarca = nome_imagem
        database.session.commit()
        flash(f'client {form.nome.data} atualizado com sucesso.')
        return redirect(url_for('cliente'))
    return render_template('editarcliente.html', form=form, client=client)


@app.route("/problema", methods=['GET', 'POST'])
@login_required
def problema():
    form_problema = FormProblema()
    lista_problema = Problema.query.filter_by(id_empresa=current_user.id_empresa)
    if form_problema.validate_on_submit() and 'btn_submit_problema' in request.form:
        problem = Problema(
            descricao=form_problema.descricao.data,
            ativo=form_problema.ativo.data,
            id_empresa=current_user.id_empresa
        )
        database.session.add(problem)
        database.session.commit()
        flash(f'Problema cadastrado com sucesso.', 'alert-success')
        return redirect(url_for('problema'))
    return render_template('problema.html', lista_problema=lista_problema, form_problema=form_problema)


@app.route("/problema/cadastro", methods=['GET', 'POST'])
@login_required
def cadastroproblema():
    form = FormProblema()    
    if form.validate_on_submit() and 'btn_submit_problema' in request.form:
        problem = Problema(
            descricao=form.descricao.data,
            ativo=form.ativo.data,
            id_empresa=current_user.id_empresa
        )
        database.session.add(problem)
        database.session.commit()
        flash(f'Problema cadastrado com sucesso.', 'alert-success')
        return redirect(url_for('problema'))
    return render_template('cadastroproblema.html', form=form)


@app.route("/problema/<problema_id>", methods=['GET', 'POST'])
@login_required
def editar_problema(problema_id):
    form = FormProblema()
    problem = Problema.query.get(problema_id)
    if form.validate_on_submit():
        problem.descricao = form.descricao.data,
        problem.ativo = form.ativo.data
        database.session.commit()
        flash(f'Problema atualizado com sucesso.', 'alert-success')
        return redirect(url_for('problema'))
    elif request.method == 'GET':
        form.descricao.data = problem.descricao
        form.ativo.data = problem.ativo
    return render_template('editarproblema.html', form=form, problem=problem)


@app.route("/setor")
@login_required
def setor():
    lista_setor = Setor.query.filter_by(id_empresa=current_user.id_empresa)
    return render_template('setor.html', lista_setor=lista_setor)


@app.route("/setor/cadastro", methods=['GET', 'POST'])
@login_required
def cadastrosetor():
    form = FormSetor()
    if form.validate_on_submit() and 'btn_submit_setor' in request.form:
        setores = Setor(
            nome=form.nome.data,
            ativo=form.ativo.data,
            id_empresa=current_user.id_empresa
        )
        database.session.add(setores)
        database.session.commit()
        flash(f'Setor {form.nome.data} cadastrado com sucesso.', 'alert-success')
        return redirect(url_for('setor'))
    return render_template('cadastrosetor.html', form=form)


@app.route("/setor/<setor_id>", methods=['GET', 'POST'])
@login_required
def editar_setor(setor_id):
    form = FormSetor()
    setores = Setor.query.get(setor_id)
    if form.validate_on_submit():
        setores.nome = form.nome.data
        setores.ativo = form.ativo.data
        database.session.commit()
        flash(f'Setor {form.nome.data} Atualizado com sucesso.', 'alert-success')
        return redirect(url_for('setor'))
    elif request.method == "GET":
        form.nome.data = setores.nome
        form.ativo.data = setores.ativo
    return render_template('editarsetor.html', form=form, setor=setores)


@app.route("/atendimento", methods=['GET', 'POST'])
@login_required
def atendimento():
    atendimentos = Atendimento.query.filter_by(id_empresa=current_user.id_empresa).order_by(Atendimento.id.desc())
    return render_template('atendimentos.html', atendimentos=atendimentos, datetime=datetime)


@app.route("/atendimento/cadastro", methods=['GET', 'POST'])
@login_required
def cadastro_atendimento():
    
    clientes = [(s.id, s.nome) for s in Cliente.query.filter_by(id_empresa=current_user.id_empresa, ativo=True)]
    problemas = [(s.id, s.descricao) for s in Problema.query.filter_by(id_empresa=current_user.id_empresa, ativo=True)]
    setores = [(s.id, s.nome) for s in Setor.query.filter_by(id_empresa=current_user.id_empresa, ativo=True)]
    protocolo = Atendimento.query.filter_by(id_empresa=current_user.id_empresa)
    form = FormAtendimento(request.form)
    form.setor.choices = setores
    form.cliente.choices = clientes
    form.problema.choices = problemas
    print(protocolo)
    print(request.form.get('cliente'))
    if form.validate_on_submit() and 'btn_submit_novo' in request.form:
        new_atendimento = Atendimento(
            protocolo=1,
            data_vencimento=form.data_vencimento.data,
            observacao=form.observacao.data,
            prioridade=form.prioridade.data,
            solicitante=form.solicitante.data,
            id_empresa=current_user.id_empresa,
            id_usuario=current_user.id,
            id_problema=request.form.get('problema'),
            id_cliente=request.form.get('cliente'),
            id_setor=request.form.get('setor'))
        database.session.add(new_atendimento)
        database.session.commit()
        flash(f'Atendimento cadastrado com sucesso.', 'alert-success')
        return redirect(url_for('atendimento'))
    return render_template('cadastro_atendimento.html', form=form)


@app.route('/atendimento/<atendimento_id>', methods=['GET', 'POST'])
@login_required
def visualizar_atendimento(atendimento_id):
    form = FormComentario()
    form_cancel = FormCancelamento()
    form_fechar = FormFecharAtendimento()
    problemas = [(s.id, s.descricao) for s in Problema.query.filter_by(id_empresa=current_user.id_empresa, ativo=True)]
    usuarios = [(s.id, s.username) for s in Usuario.query.filter_by(id_empresa=current_user.id_empresa, ativo=True)]
    form.usuario.choices = usuarios
    form.problema.choices = problemas
    atend = Atendimento.query.get(atendimento_id)
    subatend = SubAtendimento.query.filter_by(id_atendimento=atendimento_id).order_by(SubAtendimento.id.desc())
    if form.validate_on_submit() and 'btn_submit_salvar' in request.form:
        new_sub = SubAtendimento(
            id_usuario=request.form.get('usuario'),
            id_problema=request.form.get('problema'),
            observacao=form.observacao.data,
            id_atendimento=atendimento_id
        )
        database.session.add(new_sub)
        database.session.commit()
        flash(f'Comentário cadastrado com sucesso.', 'alert-success')
    elif form_cancel.validate_on_submit() and 'btn_submit_cancelar' in request.form:
        atend.data_cancelamento = datetime.utcnow()
        atend.status = 'Cancelado'
        atend.motivo_cancelamento = form_cancel.motivo.data
        coment = SubAtendimento(
            id_usuario=current_user.id,
            id_problema=atend.problema.id,
            observacao=f'{form_cancel.motivo.data}. Atendimento cancelado pelo atendente {current_user.username}.',
            id_atendimento=atendimento_id
        )
        database.session.add(coment)
        database.session.commit()
        flash('Atendimento Cancelado', 'alert-success')
        return redirect(url_for('atendimento'))
    elif form_fechar.validate_on_submit() and 'btn_submit_fechar' in request.form:
        atend.obs_fechamento = form_fechar.obs_fechamento.data
        atend.data_conclusao = datetime.utcnow()
        atend.status = 'Fechado'
        coment = SubAtendimento(
            id_usuario=current_user.id,
            id_problema=atend.problema.id,
            observacao=f'{form_fechar.obs_fechamento.data}. Atendimento finalizado pelo atendente {current_user.username}.',
            id_atendimento=atendimento_id
        )
        database.session.add(coment)
        database.session.commit()
        flash('Atendimento Concluído', 'alert-success')
        return redirect(url_for('atendimento'))
    return render_template('visualizar_atendimento.html', atendimento=atend, datetime=datetime,
                           subaten=subatend, form=form, form_cancel=form_cancel, form_fechar=form_fechar)


@app.route('/atendimento/<atendimento_id>/iniciar', methods=['GET', 'POST'])
@login_required
def iniciar_atendimento(atendimento_id):
    atendiment = Atendimento.query.get(atendimento_id)
    atendiment.data_inicio = datetime.utcnow()
    atendiment.status = 'Atendendo'
    coment = SubAtendimento(
        id_usuario=current_user.id,
        id_problema=atendiment.problema.id,
        observacao=f'Atendimento iniciado pelo atendente {current_user.username}.',
        id_atendimento=atendimento_id
    )
    database.session.add(coment)
    database.session.commit()
    flash('Atendimento iniciado', 'alert-success')
    return redirect(url_for('visualizar_atendimento', atendimento_id=atendimento_id))


@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash('Sua sessão foi encerrada.', 'alert-success')
    return redirect('login')
