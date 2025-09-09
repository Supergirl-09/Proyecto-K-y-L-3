import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

def buscar_expediente_por_id(expedientes_lista, id_buscado):
    """
    Busca un expediente en la lista por su ID.
    """
    for expediente in expedientes_lista:
        if expediente['id'] == id_buscado:
            return expediente
    return None

class RHApp:
    def __init__(self, root):
        """
        Inicializa la aplicación y la interfaz de usuario para la gestión de expedientes.
        """
        self.root = root
        self.root.title("Sistema de Gestión de Expedientes de RH")
        self.expedientes_lista = []

        frame = tk.Frame(root, padx=20, pady=20)
        frame.pack()

        tk.Label(frame, text="Sistema de Gestión de Expedientes de RH", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        tk.Button(frame, text="Agregar Nuevo Expediente", width=30, command=self.agregar_expediente_form).grid(row=1, column=0, pady=5)
        tk.Button(frame, text="Mostrar Todos los Expedientes", width=30, command=self.mostrar_expedientes).grid(row=2, column=0, pady=5)
        tk.Button(frame, text="Modificar Expediente", width=30, command=self.modificar_expediente).grid(row=3, column=0, pady=5)
        tk.Button(frame, text="Eliminar Expediente", width=30, command=self.eliminar_expediente).grid(row=4, column=0, pady=5)
        tk.Button(frame, text="Salir", width=30, command=root.quit).grid(row=5, column=0, pady=5)

    def agregar_expediente_form(self):
        """
        Muestra un formulario en una nueva ventana para agregar un expediente.
        """
        form_window = tk.Toplevel(self.root)
        form_window.title("Agregar Nuevo Expediente")
        form_window.geometry("400x300")
        form_window.transient(self.root) 
        form_window.grab_set() 

        form_frame = tk.Frame(form_window, padx=20, pady=10)
        form_frame.pack(fill="both", expand=True)

        tk.Label(form_frame, text="Nombre:").grid(row=0, column=0, sticky="w", pady=5)
        nombre_entry = tk.Entry(form_frame, width=40)
        nombre_entry.grid(row=0, column=1, pady=5)

        tk.Label(form_frame, text="RFC:").grid(row=1, column=0, sticky="w", pady=5)
        rfc_entry = tk.Entry(form_frame, width=40)
        rfc_entry.grid(row=1, column=1, pady=5)

        tk.Label(form_frame, text="CURP:").grid(row=2, column=0, sticky="w", pady=5)
        curp_entry = tk.Entry(form_frame, width=40)
        curp_entry.grid(row=2, column=1, pady=5)

        tk.Label(form_frame, text="Teléfono:").grid(row=3, column=0, sticky="w", pady=5)
        telefono_entry = tk.Entry(form_frame, width=40)
        telefono_entry.grid(row=3, column=1, pady=5)

        tk.Label(form_frame, text="Dirección:").grid(row=4, column=0, sticky="w", pady=5)
        direccion_entry = tk.Entry(form_frame, width=40)
        direccion_entry.grid(row=4, column=1, pady=5)
        
        def guardar_expediente():
            nombre = nombre_entry.get()
            rfc = rfc_entry.get()
            curp = curp_entry.get()
            telefono_str = telefono_entry.get()
            direccion = direccion_entry.get()
            
            if not nombre or not rfc or not curp or not telefono_str or not direccion:
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return

            try:
                telefono = float(telefono_str)
            except ValueError:
                messagebox.showerror("Error", "Introduce un número de teléfono válido.")
                return

            nuevo_expediente = {}
            if not self.expedientes_lista:
                nuevo_expediente['id'] = 1001
            else:
                max_id = max(exp['id'] for exp in self.expedientes_lista)
                nuevo_expediente['id'] = max_id + 1

            nuevo_expediente['nombre'] = nombre
            nuevo_expediente['RFC'] = rfc
            nuevo_expediente['CURP'] = curp
            nuevo_expediente['telefono'] = telefono
            nuevo_expediente['direccion'] = direccion

            self.expedientes_lista.append(nuevo_expediente)
            messagebox.showinfo("Éxito", f"¡Expediente agregado con éxito! El ID es: {nuevo_expediente['id']}")
            form_window.destroy()

        save_button = tk.Button(form_frame, text="Guardar", command=guardar_expediente)
        save_button.grid(row=5, column=0, pady=10)
        cancel_button = tk.Button(form_frame, text="Cancelar", command=form_window.destroy)
        cancel_button.grid(row=5, column=1, pady=10)


    def mostrar_expedientes(self):
        """
        Muestra la lista de expedientes en una nueva ventana.
        """
        if not self.expedientes_lista:
            messagebox.showinfo("Expedientes", "No hay expedientes registrados todavía.")
            return
        
        top = tk.Toplevel(self.root)
        top.title("Lista de Expedientes")

        tree = ttk.Treeview(top, columns=("ID", "Nombre", "RFC", "CURP", "Teléfono", "Dirección"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Nombre", text="Nombre")
        tree.heading("RFC", text="RFC")
        tree.heading("CURP", text="CURP")
        tree.heading("Teléfono", text="Teléfono")
        tree.heading("Dirección", text="Dirección")

        tree.column("ID", width=50)
        tree.column("Nombre", width=150)
        tree.column("RFC", width=100)
        tree.column("CURP", width=100)
        tree.column("Teléfono", width=100)
        tree.column("Dirección", width=150)

        for exp in self.expedientes_lista:
            tree.insert("", "end", values=(exp['id'], exp['nombre'], exp['RFC'], exp['CURP'], f"{exp['telefono']:.0f}", exp['direccion']))

        tree.pack(padx=10, pady=10)

    def modificar_expediente(self):
        """
        Solicita un ID y luego abre un formulario para modificar el expediente.
        """
        try:
            id_modificar = simpledialog.askinteger("Modificar", "Introduce el ID del expediente que quieres modificar:")
            if id_modificar is None:
                return
        except (TypeError, ValueError):
            messagebox.showerror("Error", "El ID debe ser un número entero.")
            return

        expediente = buscar_expediente_por_id(self.expedientes_lista, id_modificar)

        if expediente is None:
            messagebox.showerror("Error", f"No se encontró ningún expediente con el ID {id_modificar}.")
            return
        
        self.modificar_expediente_form(expediente)

    def modificar_expediente_form(self, expediente_a_modificar):
        """
        Muestra un formulario prellenado para modificar un expediente existente.
        """
        form_window = tk.Toplevel(self.root)
        form_window.title(f"Modificar Expediente ID: {expediente_a_modificar['id']}")
        form_window.geometry("400x300")
        form_window.transient(self.root)
        form_window.grab_set()

        form_frame = tk.Frame(form_window, padx=20, pady=10)
        form_frame.pack(fill="both", expand=True)

        tk.Label(form_frame, text="Nombre:").grid(row=0, column=0, sticky="w", pady=5)
        nombre_entry = tk.Entry(form_frame, width=40)
        nombre_entry.grid(row=0, column=1, pady=5)
        nombre_entry.insert(0, expediente_a_modificar['nombre'])

        tk.Label(form_frame, text="RFC:").grid(row=1, column=0, sticky="w", pady=5)
        rfc_entry = tk.Entry(form_frame, width=40)
        rfc_entry.grid(row=1, column=1, pady=5)
        rfc_entry.insert(0, expediente_a_modificar['RFC'])

        tk.Label(form_frame, text="CURP:").grid(row=2, column=0, sticky="w", pady=5)
        curp_entry = tk.Entry(form_frame, width=40)
        curp_entry.grid(row=2, column=1, pady=5)
        curp_entry.insert(0, expediente_a_modificar['CURP'])

        tk.Label(form_frame, text="Teléfono:").grid(row=3, column=0, sticky="w", pady=5)
        telefono_entry = tk.Entry(form_frame, width=40)
        telefono_entry.grid(row=3, column=1, pady=5)
        telefono_entry.insert(0, f"{expediente_a_modificar['telefono']:.0f}")

        tk.Label(form_frame, text="Dirección:").grid(row=4, column=0, sticky="w", pady=5)
        direccion_entry = tk.Entry(form_frame, width=40)
        direccion_entry.grid(row=4, column=1, pady=5)
        direccion_entry.insert(0, expediente_a_modificar['direccion'])

        def guardar_cambios():
            nuevo_nombre = nombre_entry.get()
            nuevo_rfc = rfc_entry.get()
            nuevo_curp = curp_entry.get()
            nuevo_telefono_str = telefono_entry.get()
            nueva_direccion = direccion_entry.get()

            try:
                nuevo_telefono = float(nuevo_telefono_str)
            except ValueError:
                messagebox.showerror("Error", "Introduce un número de teléfono válido.")
                return

            expediente_a_modificar['nombre'] = nuevo_nombre
            expediente_a_modificar['RFC'] = nuevo_rfc
            expediente_a_modificar['CURP'] = nuevo_curp
            expediente_a_modificar['telefono'] = nuevo_telefono
            expediente_a_modificar['direccion'] = nueva_direccion

            messagebox.showinfo("Éxito", f"¡Expediente ID {expediente_a_modificar['id']} actualizado con éxito!")
            form_window.destroy()

        save_button = tk.Button(form_frame, text="Guardar Cambios", command=guardar_cambios)
        save_button.grid(row=5, column=0, pady=10)
        cancel_button = tk.Button(form_frame, text="Cancelar", command=form_window.destroy)
        cancel_button.grid(row=5, column=1, pady=10)

    def eliminar_expediente(self):
        """
        Elimina un expediente de la lista previa confirmación.
        """
        try:
            id_eliminar = simpledialog.askinteger("Eliminar", "Introduce el ID del expediente que quieres eliminar:")
            if id_eliminar is None:
                return
        except:
            messagebox.showerror("Error", "El ID debe ser un número.")
            return

        expediente = buscar_expediente_por_id(self.expedientes_lista, id_eliminar)

        if expediente is None:
            messagebox.showerror("Error", f"No se encontró ningún expediente con el ID {id_eliminar}.")
            return

        confirmacion = messagebox.askyesno("Confirmar eliminación", f"¿Seguro que quieres eliminar a {expediente['nombre']} (ID: {id_eliminar})?")
        
        if confirmacion:
            self.expedientes_lista.remove(expediente)
            messagebox.showinfo("Éxito", "¡Expediente eliminado con éxito!")
        else:
            messagebox.showinfo("Cancelado", "Operación cancelada.")

if __name__== "__main__":
    root = tk.Tk()
    app = RHApp(root)
    root.mainloop()