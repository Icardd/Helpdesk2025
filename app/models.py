from . import db  # Garantindo que o db está sendo importado corretamente de __init__.py
from flask_login import UserMixin  # Para a classe Usuario herdar de UserMixin

class Usuario(db.Model, UserMixin):  # Herdando de db.Model e UserMixin
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)

    # Relacionamento com Chamado
    chamados = db.relationship('Chamado', back_populates="usuario")

    def __repr__(self):
        return f'<Usuario {self.email}>'


class Categoria(db.Model):
    __tablename__ = 'categorias'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)

    # Relacionamento com Chamado
    chamados = db.relationship('Chamado', back_populates="categoria")

    def __repr__(self):
        return f'<Categoria {self.nome}>'

class Dispositivo(db.Model):
    __tablename__ = 'dispositivos'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)

    # Relacionamento com Chamado
    chamados = db.relationship('Chamado', back_populates="dispositivo")

    def __repr__(self):
        return f'<Dispositivo {self.nome}>'

class Setor(db.Model):
    __tablename__ = 'setores'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)

    # Relacionamento com Chamado
    chamados = db.relationship('Chamado', back_populates="setor")

    def __repr__(self):
        return f'<Setor {self.nome}>'

class Chamado(db.Model):
    __tablename__ = 'chamados'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)
    dispositivo_id = db.Column(db.Integer, db.ForeignKey('dispositivos.id'), nullable=False)
    setor_id = db.Column(db.Integer, db.ForeignKey('setores.id'), nullable=False)
    titulo = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    prioridade = db.Column(db.Enum('Baixa', 'Média', 'Alta', name='prioridade_enum'), nullable=False)
    status = db.Column(db.Enum('Aberto', 'Em Andamento', 'Fechado', name='status_enum'), default='Aberto')
    data_abertura = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    data_fechamento = db.Column(db.TIMESTAMP, nullable=True)

    # Relacionamentos
    usuario = db.relationship('Usuario', back_populates="chamados")
    categoria = db.relationship('Categoria', back_populates="chamados")
    dispositivo = db.relationship('Dispositivo', back_populates="chamados")
    setor = db.relationship('Setor', back_populates="chamados")

    def __repr__(self):
        return f'<Chamado {self.titulo}>'