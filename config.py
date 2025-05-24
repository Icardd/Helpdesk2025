import os

class Config:
    # Configuração do banco de dados
    SQLALCHEMY_DATABASE_URI = os.getenv("mysql+pymysql://root:IEciefERnwCWjYtLDMLiqlTdDqruzEnS@mysql.railway.internal:3306/railway")
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Desativando o monitoramento de modificações do SQLAlchemy
    
    # Chave secreta para proteger a sessão do Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')  # Variável de ambiente para SECRET_KEY
    
    # Outros ajustes de configuração, caso necessário
    # Exemplo: para definir o tempo de sessão (se necessário)
    # PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
