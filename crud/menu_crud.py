from database import Session, MenuDB

def añadir_menu(nombre, descripcion, ingredientes):
    session = Session()
    nuevo_menu = MenuDB(nombre=nombre, descripcion=descripcion, ingredientes=ingredientes)
    session.add(nuevo_menu)
    session.commit()
    session.close()

def mostrar_menus():
    session = Session()
    menus = session.query(MenuDB).all()
    session.close()
    return menus

def verificar_menu_duplicado(nombre):
    session = Session()
    menu_existente = session.query(MenuDB).filter_by(nombre=nombre).first()
    session.close()
    return menu_existente is not None

def eliminar_menu(nombre):
    session = Session()
    menu_a_eliminar = session.query(MenuDB).filter_by(nombre=nombre).first()
    if menu_a_eliminar:
        session.delete(menu_a_eliminar)
        session.commit()
    session.close()