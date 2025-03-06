import customtkinter as ctk
from tkinter import messagebox
from crud.ingrediente_crud import añadir_ingrediente, mostrar_ingredientes, verificar_duplicado, eliminar_ingrediente
from crud.menu_crud import añadir_menu, mostrar_menus, verificar_menu_duplicado, eliminar_menu
from crud.cliente_crud import añadir_cliente, mostrar_clientes, verificar_cliente_duplicado, eliminar_cliente
from database import Session, MenuDB  # Asegúrate de importar MenuDB
from tkinter import ttk

# Inicializar CustomTkinter
ctk.set_appearance_mode("System")  # "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Gestión de Restaurante")
        self.geometry("1600x500")

        # Crear el contenedor de pestañas
        self.tab_control = ctk.CTkTabview(self)
        self.tab_control.pack(expand=1, fill='both')

        # Crear las pestañas
        self.tab_control.add("Ingredientes")
        self.tab_control.add("Menús")
        self.tab_control.add("Clientes")
        self.tab_control.add("Pedidos")  # Placeholder para futuras secciones
        self.tab_control.add("Estadísticas")  # Placeholder para futuras secciones

        # Configurar la pestaña de ingredientes
        self.setup_ingredients_tab()
        # Configurar la pestaña de menús
        self.setup_menus_tab()
        # Configurar la pestaña de clientes
        self.setup_clients_tab()

    def setup_ingredients_tab(self):
        # Frame para entradas
        self.frame = ctk.CTkFrame(self.tab_control.tab("Ingredientes"))
        self.frame.pack(side="left", fill="y", padx=20, pady=20)

        # Entradas
        self.label_nombre = ctk.CTkLabel(self.frame, text="Nombre:")
        self.label_nombre.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_nombre = ctk.CTkEntry(self.frame)
        self.entry_nombre.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.label_tipo = ctk.CTkLabel(self.frame, text="Tipo:")
        self.label_tipo.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_tipo = ctk.CTkEntry(self.frame)
        self.entry_tipo.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        self.label_cantidad = ctk.CTkLabel(self.frame, text="Cantidad:")
        self.label_cantidad.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_cantidad = ctk.CTkEntry(self.frame)
        self.entry_cantidad.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        self.label_unidad = ctk.CTkLabel(self.frame, text="Unidad:")
        self.label_unidad.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.entry_unidad = ctk.CTkEntry(self.frame)
        self.entry_unidad.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        # Botones
        self.btn_frame = ctk.CTkFrame(self.frame)
        self.btn_frame.grid(row=4, columnspan=2, pady=10)

        self.btn_agregar = ctk.CTkButton(self.btn_frame, text="Añadir Ingrediente", command=self.agregar_ingrediente)
        self.btn_agregar.grid(row=0, column=0, padx=5)

        self.btn_modificar = ctk.CTkButton(self.btn_frame, text="Modificar Ingrediente", command=self.modificar_ingrediente)
        self.btn_modificar.grid(row=0, column=1, padx=5)

        self.btn_eliminar = ctk.CTkButton(self.btn_frame, text="Eliminar Ingrediente", command=self.eliminar_ingrediente)
        self.btn_eliminar.grid(row=0, column=2, padx=5)

        # TreeView para mostrar ingredientes
        self.tree = ttk.Treeview(self.tab_control.tab("Ingredientes"), columns=("Nombre", "Tipo", "Cantidad", "Unidad"), show='headings')
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Tipo", text="Tipo")
        self.tree.heading("Cantidad", text="Cantidad")
        self.tree.heading("Unidad", text="Unidad")
        self.tree.pack(side="right", pady=20, padx=20, fill="both", expand=True)

        self.tree.bind("<Double-1>", self.cargar_ingrediente)

        # Cargar ingredientes al inicio
        self.actualizar_lista()

    def setup_menus_tab(self):
        # Frame para entradas
        self.frame = ctk.CTkFrame(self.tab_control.tab("Menús"))
        self.frame.pack(side="left", fill="y", padx=20, pady=20)

        # Entradas
        self.label_nombre_menu = ctk.CTkLabel(self.frame, text="Nombre del Menú:")
        self.label_nombre_menu.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_nombre_menu = ctk.CTkEntry(self.frame)
        self.entry_nombre_menu.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.label_descripcion = ctk.CTkLabel(self.frame, text="Descripción:")
        self.label_descripcion.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_descripcion = ctk.CTkEntry(self.frame)
        self.entry_descripcion.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        self.label_ingredientes = ctk.CTkLabel(self.frame, text="Ingredientes (separados por comas):")
        self.label_ingredientes.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_ingredientes = ctk.CTkEntry(self.frame)
        self.entry_ingredientes.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # Botones
        self.btn_frame_menus = ctk.CTkFrame(self.frame)
        self.btn_frame_menus.grid(row=3, columnspan=2, pady=10)

        self.btn_agregar_menu = ctk.CTkButton(self.btn_frame_menus, text="Añadir Menú", command=self.agregar_menu)
        self.btn_agregar_menu.grid(row=0, column=0, padx=5)

        self.btn_modificar_menu = ctk.CTkButton(self.btn_frame_menus, text="Modificar Menú", command=self.modificar_menu)
        self.btn_modificar_menu.grid(row=0, column=1, padx=5)

        self.btn_eliminar_menu = ctk.CTkButton(self.btn_frame_menus, text="Eliminar Menú", command=self.eliminar_menu)
        self.btn_eliminar_menu.grid(row=0, column=2, padx=5)

        # TreeView para mostrar menús
        self.tree_menus = ttk.Treeview(self.tab_control.tab("Menús"), columns=("Nombre", "Descripción", "Ingredientes"), show='headings')
        self.tree_menus.heading("Nombre", text="Nombre")
        self.tree_menus.heading("Descripción", text="Descripción")
        self.tree_menus.heading("Ingredientes", text="Ingredientes")
        self.tree_menus.pack(side="right", pady=20, padx=20, fill="both", expand=True)

        self.tree_menus.bind("<Double-1>", self.cargar_menu)

        # Cargar menús al inicio
        self.actualizar_lista_menus()

    def setup_clients_tab(self):
        # Frame para entradas
        self.frame = ctk.CTkFrame(self.tab_control.tab("Clientes"))
        self.frame.pack(side="left", fill="y", padx=20, pady=20)

        # Entradas
        self.label_nombre_cliente = ctk.CTkLabel(self.frame, text="Nombre:")
        self.label_nombre_cliente.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_nombre_cliente = ctk.CTkEntry(self.frame)
        self.entry_nombre_cliente.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.label_correo = ctk.CTkLabel(self.frame, text="Correo:")
        self.label_correo.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_correo = ctk.CTkEntry(self.frame)
        self.entry_correo.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Botones
        self.btn_frame_clients = ctk.CTkFrame(self.frame)
        self.btn_frame_clients.grid(row=2, columnspan=2, pady=10)

        self.btn_agregar_cliente = ctk.CTkButton(self.btn_frame_clients, text="Añadir Cliente", command=self.agregar_cliente)
        self.btn_agregar_cliente.grid(row=0, column=0, padx=5)

        self.btn_modificar_cliente = ctk.CTkButton(self.btn_frame_clients, text="Modificar Cliente", command=self.modificar_cliente)
        self.btn_modificar_cliente.grid(row=0, column=1, padx=5)

        self.btn_eliminar_cliente = ctk.CTkButton(self.btn_frame_clients, text="Eliminar Cliente", command=self.eliminar_cliente)
        self.btn_eliminar_cliente.grid(row=0, column=2, padx=5)

        # TreeView para mostrar clientes
        self.tree_clients = ttk.Treeview(self.tab_control.tab("Clientes"), columns=("Nombre", "Correo"), show='headings')
        self.tree_clients.heading("Nombre", text="Nombre")
        self.tree_clients.heading("Correo", text="Correo")
        self.tree_clients.pack(side="right", pady=20, padx=20, fill="both", expand=True)

        self.tree_clients.bind("<Double-1>", self.cargar_cliente)

        # Cargar clientes al inicio
        self.actualizar_lista_clientes()

    # Métodos para la gestión de ingredientes
    def agregar_ingrediente(self):
        nombre = self.entry_nombre.get().strip()
        tipo = self.entry_tipo.get().strip()
        cantidad = self.entry_cantidad.get().strip()
        unidad = self.entry_unidad.get().strip()

        # Validaciones
        if not nombre or not tipo or not cantidad or not unidad:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        if not nombre.isalpha():
            messagebox.showerror("Error", "El nombre debe contener solo letras.")
            return

        if not tipo.isalpha():
            messagebox.showerror("Error", "El tipo debe contener solo letras.")
            return

        try:
            cantidad = int(cantidad)
            if cantidad <= 0:
                messagebox.showerror("Error", "La cantidad debe ser un número entero positivo.")
                return
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número entero.")
            return

        if verificar_duplicado(nombre):
            # Si el ingrediente ya existe, fusionar cantidades
            self.fusionar_ingredientes(nombre, cantidad)
            messagebox.showinfo("Éxito", f"Ingrediente '{nombre}' actualizado correctamente.")
        else:
            añadir_ingrediente(nombre, tipo, cantidad, unidad)
            messagebox.showinfo("Éxito", f"Ingrediente '{nombre}' añadido correctamente.")

        self.actualizar_lista()
        self.limpiar_campos()

    def modificar_ingrediente(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Seleccione un ingrediente para modificar.")
            return

        item = self.tree.item(selected_item)
        nombre_actual = item['values'][0]

        nuevo_nombre = self.entry_nombre.get().strip()
        nuevo_tipo = self.entry_tipo.get().strip()
        nueva_cantidad = self.entry_cantidad.get().strip()
        nueva_unidad = self.entry_unidad.get().strip()

        # Validaciones
        if not nuevo_nombre or not nuevo_tipo or not nueva_cantidad or not nueva_unidad:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        if not nuevo_nombre.isalpha():
            messagebox.showerror("Error", "El nuevo nombre debe contener solo letras.")
            return

        try:
            nueva_cantidad = int(nueva_cantidad)
            if nueva_cantidad <= 0:
                messagebox.showerror("Error", "La cantidad debe ser un número entero positivo.")
                return
        except ValueError:
            messagebox.showerror("Error", "La cantidad debe ser un número entero.")
            return

        if nombre_actual != nuevo_nombre and verificar_duplicado(nuevo_nombre):
            messagebox.showerror("Error", "El nuevo nombre ya existe.")
            return

        # Eliminar el ingrediente actual
        eliminar_ingrediente(nombre_actual)
        # Añadir el ingrediente modificado
        añadir_ingrediente(nuevo_nombre, nuevo_tipo, nueva_cantidad, nueva_unidad)
        messagebox.showinfo("Éxito", f"Ingrediente '{nuevo_nombre}' modificado correctamente.")
        self.actualizar_lista()
        self.limpiar_campos()

    def eliminar_ingrediente(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Seleccione un ingrediente para eliminar.")
            return

        item = self.tree.item(selected_item)
        nombre = item['values'][0]
        eliminar_ingrediente(nombre)
        messagebox.showinfo("Éxito", f"Ingrediente '{nombre}' eliminado correctamente.")
        self.actualizar_lista()

    def cargar_ingrediente(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return
        item = self.tree.item(selected_item)
        nombre, tipo, cantidad, unidad = item['values']
        self.entry_nombre.delete(0, ctk.END)
        self.entry_nombre.insert(0, nombre)
        self.entry_tipo.delete(0, ctk.END)
        self.entry_tipo.insert(0, tipo)
        self.entry_cantidad.delete(0, ctk.END)
        self.entry_cantidad.insert(0, cantidad)
        self.entry_unidad.delete(0, ctk.END)
        self.entry_unidad.insert(0, unidad)

    def actualizar_lista(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        ingredientes = mostrar_ingredientes()
        for ingrediente in ingredientes:
            self.tree.insert("", "end", values=(ingrediente.nombre, ingrediente.tipo, ingrediente.cantidad, ingrediente.unidad))

    def limpiar_campos(self):
        self.entry_nombre.delete(0, ctk.END)
        self.entry_tipo.delete(0, ctk.END)
        self.entry_cantidad.delete(0, ctk.END)
        self.entry_unidad.delete(0, ctk.END)

    # Métodos para la gestión de menús
    def agregar_menu(self):
        nombre = self.entry_nombre_menu.get().strip()
        descripcion = self.entry_descripcion.get().strip()
        ingredientes = self.entry_ingredientes.get().strip()

        # Validaciones
        if not nombre or not descripcion or not ingredientes:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        if not nombre.isalpha():
            messagebox.showerror("Error", "El nombre del menú debe contener solo letras.")
            return

        if verificar_menu_duplicado(nombre):
            messagebox.showerror("Error", "El menú ya existe.")
            return

        # Añadir menú
        añadir_menu(nombre, descripcion, ingredientes)
        messagebox.showinfo("Éxito", f"Menú '{nombre}' añadido correctamente.")
        self.actualizar_lista_menus()
        self.limpiar_campos_menus()

    def modificar_menu(self):
        selected_item = self.tree_menus.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Seleccione un menú para modificar.")
            return

        item = self.tree_menus.item(selected_item)
        nombre_actual = item['values'][0]

        nuevo_nombre = self.entry_nombre_menu.get().strip()
        nueva_descripcion = self.entry_descripcion.get().strip()
        nuevos_ingredientes = self.entry_ingredientes.get().strip()

        # Validaciones
        if not nuevo_nombre or not nueva_descripcion or not nuevos_ingredientes:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        if not nuevo_nombre.isalpha():
            messagebox.showerror("Error", "El nuevo nombre del menú debe contener solo letras.")
            return

        # Eliminar el menú actual
        eliminar_menu(nombre_actual)
        # Añadir el menú modificado
        añadir_menu(nuevo_nombre, nueva_descripcion, nuevos_ingredientes)
        messagebox.showinfo("Éxito", f"Menú '{nuevo_nombre}' modificado correctamente.")
        self.actualizar_lista_menus()
        self.limpiar_campos_menus()

    def eliminar_menu(self):
        selected_item = self.tree_menus.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Seleccione un menú para eliminar.")
            return

        item = self.tree_menus.item(selected_item)
        nombre = item['values'][0]
        eliminar_menu(nombre)
        messagebox.showinfo("Éxito", f"Menú '{nombre}' eliminado correctamente.")
        self.actualizar_lista_menus()

    def cargar_menu(self, event):
        selected_item = self.tree_menus.selection()
        if not selected_item:
            return
        item = self.tree_menus.item(selected_item)
        nombre, descripcion, ingredientes = item['values']
        self.entry_nombre_menu.delete(0, ctk.END)
        self.entry_nombre_menu.insert(0, nombre)
        self.entry_descripcion.delete(0, ctk.END)
        self.entry_descripcion.insert(0, descripcion)
        self.entry_ingredientes.delete(0, ctk.END)
        self.entry_ingredientes.insert(0, ingredientes)

    def actualizar_lista_menus(self):
        for item in self.tree_menus.get_children():
            self.tree_menus.delete(item)
        menus = mostrar_menus()
        for menu in menus:
            self.tree_menus.insert("", "end", values=(menu.nombre, menu.descripcion, menu.ingredientes))

    def limpiar_campos_menus(self):
        self.entry_nombre_menu.delete(0, ctk.END)
        self.entry_descripcion.delete(0, ctk.END)
        self.entry_ingredientes.delete(0, ctk.END)

    # Métodos para la gestión de clientes
    def agregar_cliente(self):
        nombre = self.entry_nombre_cliente.get().strip()
        correo = self.entry_correo.get().strip()

        # Validaciones
        if not nombre or not correo:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        if verificar_cliente_duplicado(correo):
            messagebox.showerror("Error", "El cliente ya existe.")
            return

        # Añadir cliente
        añadir_cliente(nombre, correo)
        messagebox.showinfo("Éxito", f"Cliente '{nombre}' añadido correctamente.")
        self.actualizar_lista_clientes()
        self.limpiar_campos_clientes()

    def modificar_cliente(self):
        selected_item = self.tree_clients.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Seleccione un cliente para modificar.")
            return

        item = self.tree_clients.item(selected_item)
        correo_actual = item['values'][1]

        nuevo_nombre = self.entry_nombre_cliente.get().strip()
        nuevo_correo = self.entry_correo.get().strip()

        # Validaciones
        if not nuevo_nombre or not nuevo_correo:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        # Eliminar el cliente actual
        eliminar_cliente(correo_actual)
        # Añadir el cliente modificado
        añadir_cliente(nuevo_nombre, nuevo_correo)
        messagebox.showinfo("Éxito", f"Cliente '{nuevo_nombre}' modificado correctamente.")
        self.actualizar_lista_clientes()
        self.limpiar_campos_clientes()

    def eliminar_cliente(self):
        selected_item = self.tree_clients.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Seleccione un cliente para eliminar.")
            return

        item = self.tree_clients.item(selected_item)
        correo = item['values'][1]
        eliminar_cliente(correo)
        messagebox.showinfo("Éxito", f"Cliente con correo '{correo}' eliminado correctamente.")
        self.actualizar_lista_clientes()

    def cargar_cliente(self, event):
        selected_item = self.tree_clients.selection()
        if not selected_item:
            return
        item = self.tree_clients.item(selected_item)
        nombre, correo = item['values']
        self.entry_nombre_cliente.delete(0, ctk.END)
        self.entry_nombre_cliente.insert(0, nombre)
        self.entry_correo.delete(0, ctk.END)
        self.entry_correo.insert(0, correo)

    def actualizar_lista_clientes(self):
        for item in self.tree_clients.get_children():
            self.tree_clients.delete(item)
        clientes = mostrar_clientes()
        for cliente in clientes:
            self.tree_clients.insert("", "end", values=(cliente.nombre, cliente.correo))

    def limpiar_campos_clientes(self):
        self.entry_nombre_cliente.delete(0, ctk.END)
        self.entry_correo.delete(0, ctk.END)

if __name__ == "__main__":
    app = App()
    app.mainloop()