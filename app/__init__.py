# __init__.py
from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# Instanciando as bibliotecas necessárias
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

# Configuração do Flask-Login
login_manager.login_view = 'main.login'  # Redireciona para a página de login se o usuário não estiver autenticado

# Função user_loader para o Flask-Login
@login_manager.user_loader
def load_user(user_id):
    from .models import Usuario  # IMPORTAÇÃO AQUI DENTRO AGORA 
    return Usuario.query.get(int(user_id))  # Carrega o usuário com base no ID

def create_app():
    # Criando a instância do Flask
    app = Flask(
        __name__,
        template_folder=os.path.join(os.path.dirname(__file__), '..', 'templates'),
        static_folder=os.path.join(os.path.dirname(__file__), '..', 'static')
    )

    # Carregando as configurações do app
    from config import Config
    app.config.from_object(Config)

    # Inicializando as extensões do Flask
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Registrando o Blueprint para as rotas
    from app.routes import main
    app.register_blueprint(main)

    return app