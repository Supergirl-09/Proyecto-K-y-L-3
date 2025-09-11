import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
###########Esta es la explicacion real la explicacion real la explicacion real
#primero aqui añado la libreria de csv de python para poder trabajar con ella
import csv #<-Eso de ahi :D

#despues de eso vamos a ponerle un nombre al archivo de excel definiendolo
ARCHIVO_CSV = 'expedientes.csv' #le puse expedientes pero si te parece mejor
#otro nombre entonces adelante, lo puedes cambiar

def buscar_expediente_por_id(expedientes_lista, id_buscado):
    """
    Busca un expediente en la lista por su ID.
    """
    for expediente in expedientes_lista:
        if expediente.get('id') == id_buscado:
            return expediente
    return None

class RHApp:
    def __init__(self, root):
        """
        Inicializa la aplicación y la interfaz de usuario con el menú universal.
        """
        self.root = root
        self.root.title("Sistema de Gestión de Expedientes de RH")
        self.root.geometry("800x600")
        self.expedientes_lista = []

        # Configuración del estilo de la aplicación
        self.style = ttk.Style()
        self.style.theme_use('clam')  # 'clam' es un tema moderno
        
        # Colores y fuentes
        main_bg_color = '#F5F7FA'
        frame_bg_color = '#FFFFFF'
        button_bg_color = '#3498DB'
        button_fg_color = '#ECF0F1'
        
        self.style.configure('TFrame', background=main_bg_color)
        self.style.configure('TButton', font=('Arial', 12, 'bold'), background=button_bg_color, foreground=button_fg_color, padding=10, relief='flat')
        self.style.map('TButton', background=[('active', '#2980B9')])
        self.style.configure('TLabel', background=frame_bg_color, font=('Arial', 12))
        self.style.configure('TEntry', font=('Arial', 12))

        #aki sigue el paso 4
        #aqui cargamos los expedientes al iniciar
        self.cargar_expedientes()
        #configuarmos la accion q se hace al cerrar ventana pa guardar
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # El menú universal es ahora el punto de entrada de la aplicación
        self.mostrar_menu_universal()
    
    #aki va el paso 4
    def on_closing(self):
        """Función que se llama al intentar cerrar la ventana."""
        if messagebox.askyesno("Salir", "¿Quieres guardar los cambios y salir?"):
            self.guardar_expedientes()
            self.root.destroy()
        else:
            self.root.destroy()

    #ahora toca el paso 2 :D que es ammm
    #crear la funcion para poder guardar los datos
    #vamos a crear un nuevo metodo en la clase de RHApp y le vamos a poner
    #guardar_expdientes (asi c entiende bien xd) esto lo que hace es queee
    #escribe la lista de self.expedientes_lista en el archivo d csv (excel ps)
    #usaremos with open() para que el archivo sea seguro
    #haremos un csv.writer para escribir los datos
    #vamos a definir el orden de las columnas en una lista, metiendo todos los campos
    #vamos a escribir la cabecera d las columnas con writer.writerow(columnas)
    #para cada expediente se van a extraer los datos personales y organizacionales
    #y se van a unir en una sola lista para escribir la fila
    def guardar_expedientes(self):
        """Guarda los expedientes en un archivo CSV."""
        if not self.expedientes_lista:
            # Si la lista está vacía, se crea un archivo vacío con solo el encabezado
            with open(ARCHIVO_CSV, 'w', newline='', encoding='utf-8') as archivo:
                writer = csv.writer(archivo)
                writer.writerow(['id', 'nombre', 'RFC', 'CURP', 'telefono', 'direccion', 'puesto', 'departamento', 'jefe'])
            return
        
        columnas = [
            'id', 'nombre', 'RFC', 'CURP', 'telefono', 'direccion', 
            'puesto', 'departamento', 'jefe'
        ]

        with open(ARCHIVO_CSV, 'w', newline='', encoding='utf-8') as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(columnas)
            
            for expediente in self.expedientes_lista:
                org_data = expediente.get('organizacional', {})
                fila = [
                    expediente.get('id', ''),
                    expediente.get('nombre', ''),
                    expediente.get('RFC', ''),
                    expediente.get('CURP', ''),
                    expediente.get('telefono', ''),
                    expediente.get('direccion', ''),
                    org_data.get('puesto', ''),
                    org_data.get('departamento', ''),
                    org_data.get('jefe', '')
                ]
                escritor.writerow(fila)
        messagebox.showinfo("Guardado", "Expedientes guardados correctamente.")
    
    #aki se acaba el paso 2#
    
    #aki empiezzza el paso 3 xd#
    #aqui tenemos que crear un metodo para leer los datos del archivo csv
    #cuando la app se inicie, le vamos ap oner cargar_expedientes
    #soy muy original lo se uwu
    #con try-except manejamos el caso en el cual no exista archivo =v
    #con csv.reader lo leermos fila x fila
    #tenemos que hacer un diccionario para cada expediente, con la estructura de los datos
    #tmb los campos organizacionales
    #los datos como id o telefono hay q pasarlos a int o float, q convertirlos pues
    def cargar_expedientes(self):
        """Carga los expedientes desde un archivo CSV."""
        try:
            with open(ARCHIVO_CSV, 'r', encoding='utf-8') as archivo:
                lector = csv.reader(archivo)
                encabezados = next(lector)  # Lee la primera fila de encabezados
                self.expedientes_lista.clear()
                
                for fila in lector:
                    expediente = {}
                    expediente['id'] = int(fila[0])
                    expediente['nombre'] = fila[1]
                    expediente['RFC'] = fila[2]
                    expediente['CURP'] = fila[3]
                    expediente['telefono'] = float(fila[4])
                    expediente['direccion'] = fila[5]
                    
                    expediente['organizacional'] = {
                        'puesto': fila[6],
                        'departamento': fila[7],
                        'jefe': fila[8]
                    }
                    self.expedientes_lista.append(expediente)
            messagebox.showinfo("Cargado", "Expedientes cargados correctamente.")
        except FileNotFoundError:
            messagebox.showinfo("Cargado", "No se encontró un archivo de expedientes. Se creará uno nuevo al guardar.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al cargar el archivo: {e}")
    #aki se acaba el paso 3#

    def mostrar_menu_universal(self):
        """
        Crea y muestra el menú principal con las dos opciones: Personal y Organizacional.
        """
        self.limpiar_ventana()
        frame = ttk.Frame(self.root, padding=50, style='TFrame')
        frame.pack(expand=True, fill='both')
        title_label = ttk.Label(frame, text="Sistema de Gestión de RH", font=("Arial", 20, "bold"), background='#F5F7FA')
        title_label.pack(pady=20)
        subtitle_label = ttk.Label(frame, text="Seleccione el tipo de expediente que desea gestionar:", font=("Arial", 12), background='#F5F7FA')
        subtitle_label.pack(pady=10)
        button_frame = ttk.Frame(frame, padding=20)
        button_frame.pack(pady=20)
        ttk.Button(button_frame, text="Expediente Personal", width=30, command=self.mostrar_menu_personal).pack(pady=10)
        ttk.Button(button_frame, text="Expediente Organizacional", width=30, command=self.mostrar_menu_organizacional).pack(pady=10)
        ttk.Button(button_frame, text="Salir", width=30, command=self.root.quit).pack(pady=10)
    
    def mostrar_menu_personal(self):
        """
        Muestra el menú para la gestión de expedientes personales.
        """
        self.limpiar_ventana()
        frame = ttk.Frame(self.root, padding=50, style='TFrame')
        frame.pack(expand=True, fill='both')
        title_label = ttk.Label(frame, text="Gestión de Expedientes Personales", font=("Arial", 18, "bold"), background='#F5F7FA')
        title_label.pack(pady=20)
        button_frame = ttk.Frame(frame, padding=20)
        button_frame.pack(pady=20)
        ttk.Button(button_frame, text="Agregar Nuevo Expediente", width=30, command=self.agregar_expediente_form).pack(pady=5)
        ttk.Button(button_frame, text="Mostrar Todos los Expedientes", width=30, command=self.mostrar_expedientes).pack(pady=5)
        ttk.Button(button_frame, text="Modificar Expediente", width=30, command=self.modificar_expediente).pack(pady=5)
        ttk.Button(button_frame, text="Eliminar Expediente", width=30, command=self.eliminar_expediente).pack(pady=5)
        ttk.Button(button_frame, text="Volver al Menú Principal", width=30, command=self.mostrar_menu_universal).pack(pady=15)
    
    def mostrar_menu_organizacional(self):
        """
        Muestra el menú para la gestión de datos organizacionales.
        """
        self.limpiar_ventana()
        frame = ttk.Frame(self.root, padding=50, style='TFrame')
        frame.pack(expand=True, fill='both')
        title_label = ttk.Label(frame, text="Gestión de Datos Organizacionales", font=("Arial", 18, "bold"), background='#F5F7FA')
        title_label.pack(pady=20)
        button_frame = ttk.Frame(frame, padding=20)
        button_frame.pack(pady=20)
        ttk.Button(button_frame, text="Agregar/Modificar Datos Organizacionales", width=40, command=self.agregar_datos_organizacionales_form).pack(pady=5)
        ttk.Button(button_frame, text="Volver al Menú Principal", width=40, command=self.mostrar_menu_universal).pack(pady=15)
    
    def limpiar_ventana(self):
        """
        Limpia todos los widgets de la ventana principal.
        """
        for widget in self.root.winfo_children():
            widget.destroy()

    def agregar_expediente_form(self):
        """
        Muestra un formulario para agregar un expediente personal.
        """
        form_window = tk.Toplevel(self.root)
        form_window.title("Agregar Nuevo Expediente")
        form_window.geometry("400x350")
        form_window.transient(self.root)
        form_window.grab_set()
        form_frame = ttk.Frame(form_window, padding=20)
        form_frame.pack(expand=True, fill='both')
        field_names = ["Nombre:", "RFC:", "CURP:", "Teléfono:", "Dirección:"]
        entries = {}
        for i, name in enumerate(field_names):
            ttk.Label(form_frame, text=name).grid(row=i, column=0, sticky="w", pady=5)
            entry = ttk.Entry(form_frame, width=40)
            entry.grid(row=i, column=1, pady=5)
            entries[name.replace(':', '')] = entry
        
        def guardar_expediente():
            nombre = entries['Nombre'].get()
            rfc = entries['RFC'].get()
            curp = entries['CURP'].get()
            telefono_str = entries['Teléfono'].get()
            direccion = entries['Dirección'].get()
            if not all([nombre, rfc, curp, telefono_str, direccion]):
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
            nuevo_expediente['organizacional'] = {}
            self.expedientes_lista.append(nuevo_expediente)
            messagebox.showinfo("Éxito", f"¡Expediente personal agregado con éxito! El ID es: {nuevo_expediente['id']}")
            form_window.destroy()
        save_button = ttk.Button(form_frame, text="Guardar", command=guardar_expediente)
        save_button.grid(row=5, column=0, pady=10)
        cancel_button = ttk.Button(form_frame, text="Cancelar", command=form_window.destroy)
        cancel_button.grid(row=5, column=1, pady=10)
    
    def agregar_datos_organizacionales_form(self):
        """
        Solicita un ID y, si lo encuentra, abre un formulario para agregar datos organizacionales.
        """
        try:
            id_buscado = simpledialog.askinteger("Datos Organizacionales", "Introduce el ID del expediente que quieres actualizar:")
            if id_buscado is None:
                return
        except (TypeError, ValueError):
            messagebox.showerror("Error", "El ID debe ser un número entero.")
            return
        expediente = buscar_expediente_por_id(self.expedientes_lista, id_buscado)
        if expediente is None:
            messagebox.showerror("Error", f"No se encontró ningún expediente con el ID {id_buscado}.")
            return
        self.abrir_form_organizacional(expediente)

    def abrir_form_organizacional(self, expediente_a_modificar):
        """
        Muestra un formulario para agregar/modificar los datos organizacionales del expediente.
        """
        form_window = tk.Toplevel(self.root)
        form_window.title(f"Datos Organizacionales para ID: {expediente_a_modificar['id']}")
        form_window.geometry("400x250")
        form_window.transient(self.root)
        form_window.grab_set()
        form_frame = ttk.Frame(form_window, padding=20)
        form_frame.pack(expand=True, fill='both')
        ttk.Label(form_frame, text=f"Expediente de: {expediente_a_modificar['nombre']}", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        field_names = ["Puesto:", "Departamento:", "Jefe Superior:"]
        entries = {}
        org_data = expediente_a_modificar.get('organizacional', {})
        initial_values = [org_data.get('puesto', ''), org_data.get('departamento', ''), org_data.get('jefe', '')]
        for i, name in enumerate(field_names):
            ttk.Label(form_frame, text=name).grid(row=i+1, column=0, sticky="w", pady=5)
            entry = ttk.Entry(form_frame, width=40)
            entry.grid(row=i+1, column=1, pady=5)
            entry.insert(0, initial_values[i])
            entries[name.replace(':', '')] = entry
        def guardar_organizacional():
            puesto = entries['Puesto'].get()
            departamento = entries['Departamento'].get()
            jefe = entries['Jefe Superior'].get()
            if not all([puesto, departamento, jefe]):
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return
            expediente_a_modificar['organizacional']['puesto'] = puesto
            expediente_a_modificar['organizacional']['departamento'] = departamento
            expediente_a_modificar['organizacional']['jefe'] = jefe
            messagebox.showinfo("Éxito", "Datos organizacionales actualizados con éxito!")
            form_window.destroy()
        save_button = ttk.Button(form_frame, text="Guardar Cambios", command=guardar_organizacional)
        save_button.grid(row=len(field_names) + 1, column=0, pady=10)
        cancel_button = ttk.Button(form_frame, text="Cancelar", command=form_window.destroy)
        cancel_button.grid(row=len(field_names) + 1, column=1, pady=10)
    
    def mostrar_expedientes(self):
        """
        Muestra la lista completa de expedientes, incluyendo datos personales y organizacionales.
        """
        if not self.expedientes_lista:
            messagebox.showinfo("Expedientes", "No hay expedientes registrados todavía.")
            return
        top = tk.Toplevel(self.root)
        top.title("Lista de Expedientes")
        top.geometry("1100x500")
        tree = ttk.Treeview(top, columns=("ID", "Nombre", "RFC", "CURP", "Teléfono", "Dirección", "Puesto", "Departamento", "Jefe Superior"), show="headings")
        tree.pack(fill="both", expand=True, padx=20, pady=20)
        headings = {
            "ID": "ID", "Nombre": "Nombre", "RFC": "RFC", "CURP": "CURP",
            "Teléfono": "Teléfono", "Dirección": "Dirección", "Puesto": "Puesto",
            "Departamento": "Departamento", "Jefe Superior": "Jefe Superior"
        }
        for col, text in headings.items():
            tree.heading(col, text=text)
            tree.column(col, width=100)
        tree.column("ID", width=50, anchor='center')
        tree.column("Nombre", width=120)
        tree.column("Dirección", width=150)
        tree.column("Jefe Superior", width=120)
        for exp in self.expedientes_lista:
            org_data = exp.get('organizacional', {})
            values = (
                exp.get('id', ''), exp.get('nombre', ''), exp.get('RFC', ''), exp.get('CURP', ''),
                f"{exp.get('telefono', 0):.0f}", exp.get('direccion', ''),
                org_data.get('puesto', 'N/A'), org_data.get('departamento', 'N/A'), org_data.get('jefe', 'N/A')
            )
            tree.insert("", "end", values=values)
    
    def modificar_expediente(self):
        try:
            id_modificar = simpledialog.askinteger("Modificar", "Introduce el ID del expediente que quieres modificar:")
            if id_modificar is None: return
        except (TypeError, ValueError):
            messagebox.showerror("Error", "El ID debe ser un número entero.")
            return
        expediente = buscar_expediente_por_id(self.expedientes_lista, id_modificar)
        if expediente is None:
            messagebox.showerror("Error", f"No se encontró ningún expediente con el ID {id_modificar}.")
            return
        self.modificar_expediente_form(expediente)

    def modificar_expediente_form(self, expediente_a_modificar):
        form_window = tk.Toplevel(self.root)
        form_window.title(f"Modificar Expediente ID: {expediente_a_modificar['id']}")
        form_window.geometry("400x350")
        form_window.transient(self.root)
        form_window.grab_set()
        form_frame = ttk.Frame(form_window, padding=20)
        form_frame.pack(expand=True, fill='both')
        field_names = ["Nombre:", "RFC:", "CURP:", "Teléfono:", "Dirección:"]
        entries = {}
        initial_values = [expediente_a_modificar.get(key, '') for key in ['nombre', 'RFC', 'CURP', 'telefono', 'direccion']]
        for i, name in enumerate(field_names):
            ttk.Label(form_frame, text=name).grid(row=i, column=0, sticky="w", pady=5)
            entry = ttk.Entry(form_frame, width=40)
            entry.grid(row=i, column=1, pady=5)
            entry.insert(0, initial_values[i] if name != "Teléfono:" else f"{expediente_a_modificar.get('telefono', 0):.0f}")
            entries[name.replace(':', '')] = entry
        def guardar_cambios():
            nuevo_nombre = entries['Nombre'].get()
            nuevo_rfc = entries['RFC'].get()
            nuevo_curp = entries['CURP'].get()
            nuevo_telefono_str = entries['Teléfono'].get()
            nueva_direccion = entries['Dirección'].get()
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
        save_button = ttk.Button(form_frame, text="Guardar Cambios", command=guardar_cambios)
        save_button.grid(row=5, column=0, pady=10)
        cancel_button = ttk.Button(form_frame, text="Cancelar", command=form_window.destroy)
        cancel_button.grid(row=5, column=1, pady=10)

    def eliminar_expediente(self):
        try:
            id_eliminar = simpledialog.askinteger("Eliminar", "Introduce el ID del expediente que quieres eliminar:")
            if id_eliminar is None: return
        except:
            messagebox.showerror("Error", "El ID debe ser un número.")
            return
        expediente = buscar_expediente_por_id(self.expedientes_lista, id_eliminar)
        if expediente is None:
            messagebox.showerror("Error", f"No se encontró ningún expediente con el ID {id_eliminar}.")
            return
        confirmacion = messagebox.askyesno("Confirmar eliminación", f"¿Seguro que quieres eliminar a {expediente.get('nombre', '')} (ID: {id_eliminar})?")
        if confirmacion:
            self.expedientes_lista.remove(expediente)
            messagebox.showinfo("Éxito", "¡Expediente eliminado con éxito!")
        else:
            messagebox.showinfo("Cancelado", "Operación cancelada.")

if __name__== "__main__":
    root = tk.Tk()
    app = RHApp(root)
    root.mainloop()