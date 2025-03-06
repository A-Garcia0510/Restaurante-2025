# database.py

from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class IngredienteDB(Base):
    __tablename__ = 'ingredientes'
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String, unique=True)
    tipo = Column(String)
    cantidad = Column(Integer)
    unidad = Column(String)
    

class MenuDB(Base):
    __tablename__ = 'menus'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, unique=True, nullable=False)
    descripcion = Column(String, nullable=False)
    ingredientes = Column(String, nullable=False)  # Puedes usar un formato como JSON o una cadena separada por comas

    def __repr__(self):
        return f"<Menu(nombre={self.nombre}, descripcion={self.descripcion}, ingredientes={self.ingredientes})>"

class ClienteDB(Base):
    __tablename__ = 'clientes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    correo = Column(String, unique=True, nullable=False)

    def __repr__(self):
        return f"<Cliente(nombre={self.nombre}, correo={self.correo})>"
    
class PedidoDB(Base):
    __tablename__ = 'pedidos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente = Column(String, nullable=False)
    menu = Column(String, nullable=False)
    cantidad = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<Pedido(cliente={self.cliente}, menu={self.menu}, cantidad={self.cantidad})>"

# Configuración de la base de datos
engine = create_engine('sqlite:///restaurante.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)