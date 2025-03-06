# main.py

from database import engine, Base

def main():
    # Crear las tablas en la base de datos
    Base.metadata.create_all(engine)
    print("Base de datos y tablas creadas correctamente.")

if __name__ == "__main__":
    main()