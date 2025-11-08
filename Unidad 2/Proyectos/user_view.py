# user_view.py
import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
import subprocess
import sys
import os

# Configurar rutas
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

try:
    from navigation import volver_dashboard, volver_login
    NAVIGATION_AVAILABLE = True
except ImportError as e:
    print(f"Navigation no disponible: {e}")
    NAVIGATION_AVAILABLE = False

def crear_conexion():
    try:
        return mysql.connector.connect(
            host='localhost',
            database='poo_proyecto_parcial2',
            user='root',
            password=''
        )
    except:
        return None

def ver_usuarios():
    conexion = crear_conexion()
    if not conexion:
        return []
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT id, username, nombre FROM usuarios")
        return cursor.fetchall()
    except:
        return []
    finally:
        if conexion:
            conexion.close()

def agregar_usuario(username, password, nombre):
    conexion = crear_conexion()
    if not conexion:
        return False
    try:
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO usuarios (username, password, nombre) VALUES (%s, %s, %s)", 
                      (username, password, nombre))
        conexion.commit()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        if conexion:
            conexion.close()

def actualizar_usuario(id_usuario, username, password, nombre):
    conexion = crear_conexion()
    if not conexion:
        return False
    try:
        cursor = conexion.cursor()
        cursor.execute("UPDATE usuarios SET username=%s, password=%s, nombre=%s WHERE id=%s", 
                      (username, password, nombre, id_usuario))
        conexion.commit()
        return True
    except:
        return False
    finally:
        if conexion:
            conexion.close()

def eliminar_usuario(id_usuario):
    conexion = crear_conexion()
    if not conexion:
        return False
    try:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id=%s", (id_usuario,))
        conexion.commit()
        return True
    except:
        return False
    finally:
        if conexion:
            conexion.close()

class UserApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Gestión de Usuarios")
        self.root.geometry("700x500")
        
        # Centrar ventana
        self.root.eval('tk::PlaceWindow . center')
        
        self.crear_elementos()
        self.ver_usuarios()
        self.root.mainloop()

    def crear_elementos(self):
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        tk.Label(main_frame, text="Gestión de Usuarios", 
                font=("Arial", 16, "bold")).pack(pady=10)

        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Agregar Usuario", command=self.agregar_usuario, 
                 bg="green", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Ver Usuarios", command=self.ver_usuarios,
                 bg="blue", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Actualizar Usuario", command=self.actualizar_usuario,
                 bg="orange", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Eliminar Usuario", command=self.eliminar_usuario,
                 bg="red", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Volver al Dashboard", command=self.volver_menu,
                 bg="purple", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Cerrar Sesión", command=self.cerrar_sesion,
                 bg="gray", fg="white").pack(side=tk.LEFT, padx=5)

        self.tree = ttk.Treeview(main_frame, columns=("ID", "Usuario", "Nombre"), 
                               show="headings", height=15)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Usuario", text="Usuario")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.column("ID", width=50)
        self.tree.column("Usuario", width=100)
        self.tree.column("Nombre", width=200)
        self.tree.pack(fill="both", expand=True, pady=10)

    def agregar_usuario(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Agregar Usuario")
        add_window.geometry("300x250")
        add_window.eval('tk::PlaceWindow . center')

        tk.Label(add_window, text="Username:").pack(pady=5)
        username_entry = tk.Entry(add_window, width=30)
        username_entry.pack(pady=5)

        tk.Label(add_window, text="Contraseña:").pack(pady=5)
        password_entry = tk.Entry(add_window, width=30, show="*")
        password_entry.pack(pady=5)

        tk.Label(add_window, text="Nombre:").pack(pady=5)
        nombre_entry = tk.Entry(add_window, width=30)
        nombre_entry.pack(pady=5)

        def guardar():
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            nombre = nombre_entry.get().strip()

            if not username or not password:
                messagebox.showerror("Error", "Username y contraseña son obligatorios")
                return

            if agregar_usuario(username, password, nombre):
                messagebox.showinfo("Éxito", "Usuario agregado correctamente")
                add_window.destroy()
                self.ver_usuarios()
            else:
                messagebox.showerror("Error", "Error al agregar usuario")

        btn_frame = tk.Frame(add_window)
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="Guardar", command=guardar, bg="green", fg="white").pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Cancelar", command=add_window.destroy, bg="red", fg="white").pack(side=tk.LEFT, padx=10)

    def ver_usuarios(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        usuarios = ver_usuarios()
        for u in usuarios:
            self.tree.insert("", tk.END, values=u)

    def actualizar_usuario(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un usuario")
            return

        item = seleccion[0]
        datos = self.tree.item(item, 'values')

        update_window = tk.Toplevel(self.root)
        update_window.title("Actualizar Usuario")
        update_window.geometry("300x250")
        update_window.eval('tk::PlaceWindow . center')

        tk.Label(update_window, text="Username:").pack(pady=5)
        username_entry = tk.Entry(update_window, width=30)
        username_entry.insert(0, datos[1])
        username_entry.pack(pady=5)

        tk.Label(update_window, text="Contraseña:").pack(pady=5)
        password_entry = tk.Entry(update_window, width=30, show="*")
        password_entry.insert(0, "********")
        password_entry.pack(pady=5)

        tk.Label(update_window, text="Nombre:").pack(pady=5)
        nombre_entry = tk.Entry(update_window, width=30)
        nombre_entry.insert(0, datos[2])
        nombre_entry.pack(pady=5)

        def guardar_cambios():
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            nombre = nombre_entry.get().strip()

            if not username:
                messagebox.showerror("Error", "Username es obligatorio")
                return

            if password == "********":
                conexion = crear_conexion()
                if conexion:
                    try:
                        cursor = conexion.cursor()
                        cursor.execute("SELECT password FROM usuarios WHERE id=%s", (datos[0],))
                        resultado = cursor.fetchone()
                        password = resultado[0] if resultado else ""
                    except:
                        password = ""
                    finally:
                        conexion.close()

            if actualizar_usuario(datos[0], username, password, nombre):
                messagebox.showinfo("Éxito", "Usuario actualizado correctamente")
                update_window.destroy()
                self.ver_usuarios()
            else:
                messagebox.showerror("Error", "Error al actualizar usuario")

        btn_frame = tk.Frame(update_window)
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="Guardar", command=guardar_cambios, bg="green", fg="white").pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Cancelar", command=update_window.destroy, bg="red", fg="white").pack(side=tk.LEFT, padx=10)

    def eliminar_usuario(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un usuario")
            return

        item = seleccion[0]
        datos = self.tree.item(item, 'values')

        if messagebox.askyesno("Confirmar", f"¿Eliminar usuario {datos[1]}?"):
            if eliminar_usuario(datos[0]):
                messagebox.showinfo("Éxito", "Usuario eliminado correctamente")
                self.ver_usuarios()
            else:
                messagebox.showerror("Error", "Error al eliminar usuario")

    def volver_menu(self):
        self.root.destroy()
        if NAVIGATION_AVAILABLE:
            volver_dashboard()
        else:
            # Fallback
            try:
                python = sys.executable
                dashboard_path = os.path.join(current_dir, "dashboard.py")
                if os.path.exists(dashboard_path):
                    subprocess.Popen([python, dashboard_path])
            except Exception as e:
                print(f"Error volviendo al dashboard: {e}")

    def cerrar_sesion(self):
        if messagebox.askyesno("Cerrar Sesión", "¿Está seguro de que desea cerrar sesión?"):
            self.root.destroy()
            if NAVIGATION_AVAILABLE:
                volver_login()
            else:
                # Fallback
                try:
                    python = sys.executable
                    login_path = os.path.join(current_dir, "login_view.py")
                    if os.path.exists(login_path):
                        subprocess.Popen([python, login_path])
                except Exception as e:
                    print(f"Error cerrando sesión: {e}")

if __name__ == "__main__":
    app = UserApp()