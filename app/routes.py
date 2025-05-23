from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, current_user, logout_user
from . import db
from .models import Usuario, Chamado, Dispositivo, Categoria, Setor
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Blueprint
from datetime import datetime

main = Blueprint('main', __name__)

# Rota inicial
@main.route('/')
def index():
    return redirect(url_for('main.login'))

#  Login
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        
        usuario = Usuario.query.filter_by(email=email).first()
        
        if usuario and check_password_hash(usuario.senha, senha):
            login_user(usuario)
            proxima = request.args.get('next')
            if proxima:
                return redirect(proxima)
            else:
                # Contas contendo ADMIN no email vão para a gestão, usuários normais somente para a tela de abertura
                if usuario.email.lower().startswith('admin'):
                    return redirect(url_for('main.gestao_chamados'))
                else:
                    return redirect(url_for('main.abrir_chamado'))
        else:
            flash('Email ou senha incorretos!')
            return redirect(url_for('main.login'))
    
    return render_template('login.html')

#  Cadastro de usuário
@main.route('/criar_usuario', methods=['POST'])
def criar_usuario():
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']

    # Verifica se o usuário já existe
    usuario_existente = Usuario.query.filter_by(email=email).first()
    if usuario_existente:
        flash('E-mail já cadastrado. Faça login ou use outro e-mail.')
        return redirect(url_for('main.login'))

    # Cria usuário
    senha_hash = generate_password_hash(senha)
    novo_usuario = Usuario(nome=nome, email=email, senha=senha_hash)
    db.session.add(novo_usuario)
    db.session.commit()

    flash('Conta criada com sucesso! Bem-vindo, colaborador! Faça o login para continuar.')
    return redirect(url_for('main.login'))

#  Abertura de chamado
@main.route('/abrir_chamado', methods=['GET', 'POST'])
@login_required
def abrir_chamado():
    #  Admins (técnicos) não podem abrir chamados
    if current_user.email.lower().startswith('admin'):
        flash('Técnicos não podem abrir chamados!')
        return redirect(url_for('main.gestao_chamados'))

    dispositivos = Dispositivo.query.all()
    categorias = Categoria.query.all()
    setores = Setor.query.all()

    if request.method == 'POST':
        categoria_id = request.form['categoria']
        dispositivo_id = request.form['dispositivo']
        setor_id = request.form['setor']
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        prioridade = request.form['prioridade']

        novo_chamado = Chamado(
            usuario_id=current_user.id,
            categoria_id=categoria_id,
            dispositivo_id=dispositivo_id,
            setor_id=setor_id,
            titulo=titulo,
            descricao=descricao,
            prioridade=prioridade
        )

        db.session.add(novo_chamado)
        db.session.commit()

        flash('Chamado aberto com sucesso!')
        return redirect(url_for('main.abrir_chamado'))

    return render_template('abrir_chamado.html', dispositivos=dispositivos, categorias=categorias, setores=setores)

#  Gestão de chamados (técnicos) com filtros
@main.route('/gestao_chamados', methods=['GET', 'POST'])
@login_required
def gestao_chamados():
    #  Usuário comum não acessa gestão
    if not current_user.email.lower().startswith('admin'):
        flash('Acesso restrito! Somente técnicos podem acessar a gestão de chamados.')
        return redirect(url_for('main.abrir_chamado'))

    # Filtros recebidos
    status_filter = request.args.get('status', '')
    prioridade_filter = request.args.get('prioridade', '')
    setor_filter = request.args.get('setor', '')
    data_inicio = request.args.get('data_inicio', '')
    data_fim = request.args.get('data_fim', '')

    # Filtro de chamados
    chamados_query = Chamado.query

    if status_filter:
        chamados_query = chamados_query.filter_by(status=status_filter)
    if prioridade_filter:
        chamados_query = chamados_query.filter_by(prioridade=prioridade_filter)
    if setor_filter:
        chamados_query = chamados_query.filter_by(setor_id=setor_filter)
    if data_inicio:
        try:
            data_inicio_dt = datetime.strptime(data_inicio, '%Y-%m-%d')
            chamados_query = chamados_query.filter(Chamado.data_abertura >= data_inicio_dt)
        except ValueError:
            pass  # ignora datas inválidas
    if data_fim:
        try:
            data_fim_dt = datetime.strptime(data_fim, '%Y-%m-%d')
            # Inclui até o final do dia (23:59)
            data_fim_dt = data_fim_dt.replace(hour=23, minute=59, second=59)
            chamados_query = chamados_query.filter(Chamado.data_abertura <= data_fim_dt)
        except ValueError:
            pass

    chamados = chamados_query.all()

    return render_template('gestao_chamados.html', chamados=chamados, 
                           status_filter=status_filter, prioridade_filter=prioridade_filter, 
                           setor_filter=setor_filter, data_inicio=data_inicio, data_fim=data_fim)


# Fechar chamado
@main.route('/fechar_chamado/<int:chamado_id>', methods=['POST'])
@login_required
def fechar_chamado(chamado_id):
    chamado = Chamado.query.get_or_404(chamado_id)

    # Apenas técnico pode fechar
    if not current_user.email.lower().startswith('admin'):
        flash('Ação não permitida!')
        return redirect(url_for('main.abrir_chamado'))

    # Define a data de fechamento
    chamado.data_fechamento = datetime.now()

    # Muda o status do chamado para fechado
    chamado.status = 'Fechado'
    db.session.commit()

    flash(f'Chamado {chamado.id} foi fechado com sucesso!')
    return redirect(url_for('main.gestao_chamados'))

#  Relatórios
from sqlalchemy import func

@main.route('/relatorios')
@login_required
def relatorios():
    # Somente admins (técnicos) podem acessar relatórios
    if not current_user.email.lower().startswith('admin'):
        flash('Acesso restrito! Somente técnicos podem acessar os relatórios.')
        return redirect(url_for('main.gestao_chamados'))

    # Consultas para contar os chamados de acordo com o status
    chamados_abertos = Chamado.query.filter_by(status='Aberto').count()
    chamados_atendidos = Chamado.query.filter_by(status='Fechado').count()
    
    # Para os chamados do mês, vamos pegar o mês atual e comparar com a data de abertura
    mes_atual = datetime.now().month
    chamados_mes = Chamado.query.filter(func.month(Chamado.data_abertura) == mes_atual).count()

    return render_template('relatorios.html', 
                           chamados_abertos=chamados_abertos, 
                           chamados_atendidos=chamados_atendidos, 
                           chamados_mes=chamados_mes)
#  Excluir chamado
@main.route('/excluir_chamado/<int:chamado_id>', methods=['POST'])
@login_required
def excluir_chamado(chamado_id):
    chamado = Chamado.query.get_or_404(chamado_id)

    # Verifica se é admin (técnico)
    if not current_user.email.lower().startswith('admin'):
        flash('Ação não permitida!')
        return redirect(url_for('main.gestao_chamados'))

    db.session.delete(chamado)
    db.session.commit()
    flash(f'Chamado {chamado.id} excluído com sucesso!')
    return redirect(url_for('main.gestao_chamados'))
#  Logout
@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))