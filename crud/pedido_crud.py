from database import Session, PedidoDB  # Asegúrate de importar PedidoDB correctamente

def añadir_pedido(cliente, menu, cantidad):
    session = Session()
    nuevo_pedido = PedidoDB(cliente=cliente, menu=menu, cantidad=cantidad)
    session.add(nuevo_pedido)
    session.commit()
    session.close()

def mostrar_pedidos():
    session = Session()
    pedidos = session.query(PedidoDB).all()
    session.close()
    return pedidos

def eliminar_pedido(id_pedido):
    session = Session()
    pedido_a_eliminar = session.query(PedidoDB).filter_by(id=id_pedido).first()
    if pedido_a_eliminar:
        session.delete(pedido_a_eliminar)
        session.commit()
    session.close()