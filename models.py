# models.py

class Ingrediente:
    def __init__(self, nombre, tipo, cantidad, unidad):
        self.nombre = nombre
        self.tipo = tipo
        self.cantidad = cantidad
        self.unidad = unidad

class Menu:
    def __init__(self, nombre, descripcion, ingredientes):
        self.nombre = nombre
        self.descripcion = descripcion
        self.ingredientes = ingredientes  # Puedes usar una lista o una cadena separada por comas