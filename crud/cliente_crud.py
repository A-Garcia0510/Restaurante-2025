from database import Session, ClienteDB

def añadir_cliente(nombre, correo):
    session = Session()
    nuevo_cliente = ClienteDB(nombre=nombre, correo=correo)
    session.add(nuevo_cliente)
    session.commit()
    session.close()

def mostrar_clientes():
    session = Session()
    clientes = session.query(ClienteDB).all()
    session.close()
    return clientes

def verificar_cliente_duplicado(correo):
    session = Session()
    cliente_existente = session.query(ClienteDB).filter_by(correo=correo).first()
    session.close()
    return cliente_existente is not None

def eliminar_cliente(correo):
    session = Session()
    cliente_a_eliminar = session.query(ClienteDB).filter_by(correo=correo).first()
    if cliente_a_eliminar:
        session.delete(cliente_a_eliminar)
        session.commit()
    session.close()