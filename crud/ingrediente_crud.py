# crud/ingrediente_crud.py

from database import Session, IngredienteDB

def añadir_ingrediente(nombre, tipo, cantidad, unidad):
    session = Session()
    if verificar_duplicado(nombre):
        # Si el ingrediente ya existe, fusionar cantidades
        fusionar_ingredientes(nombre, cantidad)
    else:
        nuevo_ingrediente = IngredienteDB(nombre=nombre, tipo=tipo, cantidad=cantidad, unidad=unidad)
        session.add(nuevo_ingrediente)
        session.commit()
        print(f"Ingrediente '{nombre}' añadido correctamente.")
    session.close()

def verificar_duplicado(nombre):
    session = Session()
    existe = session.query(IngredienteDB).filter_by(nombre=nombre).first() is not None
    session.close()
    return existe

def fusionar_ingredientes(nombre, cantidad):
    session = Session()
    ingrediente_existente = session.query(IngredienteDB).filter_by(nombre=nombre).first()
    if ingrediente_existente:
        # Sumar la cantidad existente con la nueva
        ingrediente_existente.cantidad += cantidad
        session.commit()
        print(f"Se ha actualizado la cantidad de '{nombre}'.")
    session.close()

def mostrar_ingredientes():
    session = Session()
    ingredientes = session.query(IngredienteDB).all()
    session.close()
    return ingredientes

def eliminar_ingrediente(nombre):
    session = Session()
    ingrediente = session.query(IngredienteDB).filter_by(nombre=nombre).first()
    if ingrediente:
        session.delete(ingrediente)
        session.commit()
        print(f"Ingrediente '{nombre}' eliminado correctamente.")
    session.close()