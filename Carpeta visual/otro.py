import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk

def buscar_empleado_por_id(empleados_lista, id_buscado):
    """
    Busca un empleado en la lista por su ID.
    """
    for empleado in empleados_lista:
        if empleado['id'] == id_buscado:
            return empleado
    return None

class RHApp:
    def __init__(self, root):
        """
        Inicializa la aplicación y la interfaz de usuario.
        """
        self.root = root
        self.root.title("Sistema de Gestión de RH")
        self.empleados_lista = []

        frame = tk.Frame(root, padx=20, pady=20)
        frame.pack()

        tk.Label(frame, text="Sistema de Gestión de RH", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        tk.Button(frame, text="Agregar Nuevo Empleado", width=30, command=self.agregar_empleado).grid(row=1, column=0, pady=5)
        tk.Button(frame, text="Mostrar Todos los Empleados", width=30, command=self.mostrar_empleados).grid(row=2, column=0, pady=5)
        tk.Button(frame, text="Modificar Empleado", width=30, command=self.modificar_empleado).grid(row=3, column=0, pady=5)
        tk.Button(frame, text="Eliminar Empleado", width=30, command=self.eliminar_empleado).grid(row=4, column=0, pady=5)
        tk.Button(frame, text="Salir", width=30, command=root.quit).grid(row=5, column=0, pady=5)

    def agregar_empleado(self):
        """
        Permite al usuario agregar un nuevo empleado a la lista.
        """
        nuevo_empleado = {}
        if not self.empleados_lista:
            nuevo_empleado['id'] = 1001
        else:
            max_id = max(emp['id'] for emp in self.empleados_lista)
            nuevo_empleado['id'] = max_id + 1
        
        messagebox.showinfo("Nuevo Empleado", f"El ID del nuevo empleado es: {nuevo_empleado['id']}")

        nombre = simpledialog.askstring("Nombre", "Introduce el nombre completo:")
        if not nombre:
            messagebox.showerror("Error", "El nombre es obligatorio.")
            return
        nuevo_empleado['nombre'] = nombre
        
        puesto = simpledialog.askstring("Puesto", "Introduce el puesto:")
        if not puesto:
            messagebox.showerror("Error", "El puesto es obligatorio.")
            return
        nuevo_empleado['puesto'] = puesto

        RFC = simpledialog.askstring("RFC", "Introduce el RFC:")
        if not RFC:
            messagebox.showerror("Error", "El RFC es obligatorio.")
            return
        nuevo_empleado['RFC'] = RFC

        CURP = simpledialog.askstring("CURP", "Introduce el CURP:")
        if not CURP:    
            messagebox.showerror("Error", "El CURP es obligatorio.")
            return
        nuevo_empleado['CURP'] = CURP
        
        while True:
            telefono = simpledialog.askstring("Teléfono", "Introduce el teléfono:")
            if not telefono:
                messagebox.showerror("Error", "Introduce un número de teléfono válido.")
                return
            nuevo_empleado['telefono'] = telefono
            break

        direccion = simpledialog.askstring("Dirección", "Introduce la dirección:")
        if not direccion:
            messagebox.showerror("Error", "La dirección es obligatoria.")
            return
        nuevo_empleado['direccion'] = direccion
                                          
        while True:
            salario_str = simpledialog.askstring("Salario", "Introduce el salario:")
            if salario_str is None:
                return
            try:
                salario = float(salario_str)
                break
            except ValueError:
                messagebox.showerror("Error", "Introduce un número válido para el salario.")
        
        nuevo_empleado['salario'] = salario
        self.empleados_lista.append(nuevo_empleado)
        messagebox.showinfo("Éxito", "¡Empleado agregado con éxito!")

    def mostrar_empleados(self):
        """
        Muestra la lista de empleados en una nueva ventana.
        """
        if not self.empleados_lista:
            messagebox.showinfo("Empleados", "No hay empleados registrados todavía.")
            return
        
        top = tk.Toplevel(self.root)
        top.title("Lista de Empleados")

        tree = ttk.Treeview(top, columns=("ID", "Nombre", "Puesto", "Salario", "RFC", "CURP", "Teléfono", "Dirección"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Nombre", text="Nombre")
        tree.heading("Puesto", text="Puesto")
        tree.heading("Salario", text="Salario")
        tree.heading("RFC", text="RFC")
        tree.heading("CURP", text="CURP")
        tree.heading("Teléfono", text="Teléfono")
        tree.heading("Dirección", text="Dirección")

        tree.column("ID", width=50)
        tree.column("Nombre", width=150)
        tree.column("Puesto", width=150)
        tree.column("Salario", width=100)
        tree.column("RFC", width=100)
        tree.column("CURP", width=100)
        tree.column("Teléfono", width=100) 
        tree.column("Dirección", width=150)

        for emp in self.empleados_lista:
            tree.insert("", "end", values=(emp['id'], emp['nombre'], emp['puesto'], f"${emp['salario']:.2f}", emp['RFC'], emp['CURP'], f"${emp['telefono']}", emp['direccion']))

        tree.pack(padx=10, pady=10)

    def modificar_empleado(self):
        """
        Permite modificar los datos de un empleado existente.
        """
        try:
            id_modificar = simpledialog.askinteger("Modificar", "Introduce el ID del empleado que quieres modificar:")
            if id_modificar is None:
                return
        except:
            messagebox.showerror("Error", "El ID debe ser un número.")
            return

        empleado = buscar_empleado_por_id(self.empleados_lista, id_modificar)

        if empleado is None:
            messagebox.showerror("Error", f"No se encontró ningún empleado con el ID {id_modificar}.")
            return
        
        nuevo_nombre = simpledialog.askstring("Nombre", f"Nuevo nombre ({empleado['nombre']}):")
        if nuevo_nombre:
            empleado['nombre'] = nuevo_nombre

        nuevo_puesto = simpledialog.askstring("Puesto", f"Nuevo puesto ({empleado['puesto']}):")
        if nuevo_puesto:
            empleado['puesto'] = nuevo_puesto
        
        while True:
            nuevo_salario_str = simpledialog.askstring("Salario", f"Nuevo salario ({empleado['salario']:.2f}):")
            if nuevo_salario_str == "" or nuevo_salario_str is None:
                break
            try:
                empleado['salario'] = float(nuevo_salario_str)
                break
            except ValueError:
                messagebox.showerror("Error", "Introduce un número válido para el salario.")
            
        if nuevo_RFC := simpledialog.askstring("RFC", f"Nuevo RFC ({empleado['RFC']}):"):
            empleado['RFC'] = nuevo_RFC

        if nuevo_CURP := simpledialog.askstring("CURP", f"Nuevo CURP ({empleado['CURP']}):"):
            empleado['CURP'] = nuevo_CURP

        while True:
           nuevo_telefono_str = simpledialog.askstring("Teléfono", f"Nuevo Teléfono ({empleado['telefono']}):")
           if nuevo_telefono_str == "" or nuevo_telefono_str is None:
               break
           try:
               empleado['telefono'] = float(nuevo_telefono_str)
               break
           except ValueError:
               messagebox.showerror("Error", "Introduce un número válido para el teléfono.")

        if nuevo_direccion := simpledialog.askstring("Dirección", f"Nuevo Dirección ({empleado['direccion']}):"):
            empleado['direccion'] = nuevo_direccion

        confirmacion = messagebox.askyesno("Confirmar modificación", f"¿Seguro que quieres modificar a {empleado['nombre']} (ID: {id_modificar})?")
        messagebox.showinfo("Éxito", "¡Empleado actualizado con éxito!")

    def eliminar_empleado(self):
        """
        Elimina un empleado de la lista previa confirmación.
        """
        try:
            id_eliminar = simpledialog.askinteger("Eliminar", "Introduce el ID del empleado que quieres eliminar:")
            if id_eliminar is None:
                return
        except:
            messagebox.showerror("Error", "El ID debe ser un número.")
            return

        empleado = buscar_empleado_por_id(self.empleados_lista, id_eliminar)

        if empleado is None:
            messagebox.showerror("Error", f"No se encontró ningún empleado con el ID {id_eliminar}.")
            return

        confirmacion = messagebox.askyesno("Confirmar eliminación", f"¿Seguro que quieres eliminar a {empleado['nombre']} (ID: {id_eliminar})?")
        
        if confirmacion:
            self.empleados_lista.remove(empleado)
            messagebox.showinfo("Éxito", "¡Empleado eliminado con éxito!")
        else:
            messagebox.showinfo("Cancelado", "Operación cancelada.")

if __name__== "__main__":
    root = tk.Tk()
    app = RHApp(root)
    root.mainloop()
