# products_view.py
import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from mysql.connector import Error
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
        conexion = mysql.connector.connect(
            host='localhost',
            database='poo_proyecto_parcial2',
            user='root',
            password=''
        )
        return conexion
    except Error as e:
        print(f"Error de conexión: {e}")
        return None

def ver_productos():
    conexion = crear_conexion()
    if not conexion:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos")
        return []
    
    try:
        cursor = conexion.cursor()
        # CORREGIDO: Usar 'description' en lugar de 'description'
        cursor.execute("SELECT id_producto, nombre_producto, stock, proveedor, precio, status, marca, description FROM productos")
        resultados = cursor.fetchall()
        return resultados
    except Error as e:
        print(f"Error al obtener productos: {e}")
        messagebox.showerror("Error", f"Error al cargar productos: {e}")
        return []
    finally:
        if conexion and conexion.is_connected():
            conexion.close()

def agregar_producto(nombre_producto, stock, proveedor, precio, status, marca, description):
    conexion = crear_conexion()
    if not conexion:
        return False, "No se pudo conectar a la base de datos"
    
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO productos 
            (nombre_producto, stock, proveedor, precio, status, marca, description) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (nombre_producto, stock, proveedor, precio, status, marca, description))
        conexion.commit()
        
        if cursor.rowcount > 0:
            return True, "Producto agregado correctamente"
        else:
            return False, "No se pudo insertar el producto"
            
    except Error as e:
        print(f"Error al agregar producto: {e}")
        conexion.rollback()
        return False, f"Error de base de datos: {e}"
    except Exception as e:
        print(f"Error inesperado: {e}")
        return False, f"Error inesperado: {e}"
    finally:
        if conexion and conexion.is_connected():
            conexion.close()

def actualizar_producto(id_producto, nombre_producto, stock, proveedor, precio, status, marca, description):
    conexion = crear_conexion()
    if not conexion:
        return False, "No se pudo conectar a la base de datos"
    
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE productos 
            SET nombre_producto=%s, stock=%s, proveedor=%s, precio=%s, 
                status=%s, marca=%s, description=%s 
            WHERE id_producto=%s
        """, (nombre_producto, stock, proveedor, precio, status, marca, description, id_producto))
        conexion.commit()
        
        if cursor.rowcount > 0:
            return True, "Producto actualizado correctamente"
        else:
            return False, "No se encontró el producto para actualizar"
            
    except Error as e:
        print(f"Error al actualizar producto: {e}")
        conexion.rollback()
        return False, f"Error de base de datos: {e}"
    finally:
        if conexion and conexion.is_connected():
            conexion.close()

def eliminar_producto(id_producto):
    conexion = crear_conexion()
    if not conexion:
        return False, "No se pudo conectar a la base de datos"
    
    try:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM productos WHERE id_producto=%s", (id_producto,))
        conexion.commit()
        
        if cursor.rowcount > 0:
            return True, "Producto eliminado correctamente"
        else:
            return False, "No se encontró el producto para eliminar"
            
    except Error as e:
        print(f"Error al eliminar producto: {e}")
        conexion.rollback()
        return False, f"Error de base de datos: {e}"
    finally:
        if conexion and conexion.is_connected():
            conexion.close()

class ProductsApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Gestión de Productos")
        self.root.geometry("1000x600")
        
        # Centrar ventana de manera compatible
        self.centrar_ventana(self.root)
        
        self.crear_elementos()
        self.ver_productos()
        self.root.mainloop()

    def centrar_ventana(self, ventana):
        """Centra una ventana en la pantalla de manera compatible"""
        ventana.update_idletasks()
        ancho = ventana.winfo_width()
        alto = ventana.winfo_height()
        x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
        y = (ventana.winfo_screenheight() // 2) - (alto // 2)
        ventana.geometry(f'+{x}+{y}')

    def crear_elementos(self):
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        tk.Label(main_frame, text="Gestión de Productos", 
                font=("Arial", 16, "bold")).pack(pady=10)

        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="➕ Agregar Producto", command=self.agregar_producto, 
                 bg="green", fg="white", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="📋 Ver Productos", command=self.ver_productos,
                 bg="blue", fg="white", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="✏️ Actualizar Producto", command=self.actualizar_producto,
                 bg="orange", fg="white", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="🗑️ Eliminar Producto", command=self.eliminar_producto,
                 bg="red", fg="white", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="📊 Volver al Dashboard", command=self.volver_dashboard,
                 bg="purple", fg="white", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="🚪 Cerrar Sesión", command=self.cerrar_sesion,
                 bg="gray", fg="white", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)

        # Treeview con todas las columnas de tu tabla
        self.tree = ttk.Treeview(main_frame, 
                               columns=("ID", "Nombre", "Stock", "Proveedor", "Precio", "Status", "Marca", "Descripción"), 
                               show="headings", height=15)
        
        # Configurar columnas
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre Producto")
        self.tree.heading("Stock", text="Stock")
        self.tree.heading("Proveedor", text="Proveedor")
        self.tree.heading("Precio", text="Precio")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Marca", text="Marca")
        self.tree.heading("Descripción", text="Descripción")
        
        self.tree.column("ID", width=50)
        self.tree.column("Nombre", width=150)
        self.tree.column("Stock", width=60)
        self.tree.column("Proveedor", width=120)
        self.tree.column("Precio", width=80)
        self.tree.column("Status", width=60)
        self.tree.column("Marca", width=100)
        self.tree.column("Descripción", width=200)
        
        self.tree.pack(fill="both", expand=True, pady=10)

    def agregar_producto(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Agregar Producto")
        add_window.geometry("400x500")
        
        # Centrar ventana de manera compatible
        self.centrar_ventana(add_window)
        add_window.grab_set()  # Hacer la ventana modal

        # Frame principal
        main_frame = tk.Frame(add_window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        tk.Label(main_frame, text="Nombre del Producto:*", font=("Arial", 10, "bold")).pack(anchor="w", pady=(5,2))
        nombre_entry = tk.Entry(main_frame, width=40, font=("Arial", 10))
        nombre_entry.pack(fill="x", pady=(0,10))
        nombre_entry.focus_set()

        tk.Label(main_frame, text="Stock:*", font=("Arial", 10, "bold")).pack(anchor="w", pady=(5,2))
        stock_entry = tk.Entry(main_frame, width=40, font=("Arial", 10))
        stock_entry.pack(fill="x", pady=(0,10))
        stock_entry.insert(0, "0")

        tk.Label(main_frame, text="Proveedor:*", font=("Arial", 10, "bold")).pack(anchor="w", pady=(5,2))
        proveedor_entry = tk.Entry(main_frame, width=40, font=("Arial", 10))
        proveedor_entry.pack(fill="x", pady=(0,10))

        tk.Label(main_frame, text="Precio:*", font=("Arial", 10, "bold")).pack(anchor="w", pady=(5,2))
        precio_entry = tk.Entry(main_frame, width=40, font=("Arial", 10))
        precio_entry.pack(fill="x", pady=(0,10))
        precio_entry.insert(0, "0")

        tk.Label(main_frame, text="Status (0=Inactivo, 1=Activo):", font=("Arial", 10, "bold")).pack(anchor="w", pady=(5,2))
        status_entry = tk.Entry(main_frame, width=40, font=("Arial", 10))
        status_entry.pack(fill="x", pady=(0,10))
        status_entry.insert(0, "1")

        tk.Label(main_frame, text="Marca:", font=("Arial", 10)).pack(anchor="w", pady=(5,2))
        marca_entry = tk.Entry(main_frame, width=40, font=("Arial", 10))
        marca_entry.pack(fill="x", pady=(0,10))

        tk.Label(main_frame, text="Descripción:", font=("Arial", 10)).pack(anchor="w", pady=(5,2))
        descripcion_entry = tk.Entry(main_frame, width=40, font=("Arial", 10))
        descripcion_entry.pack(fill="x", pady=(0,10))

        def guardar():
            try:
                nombre = nombre_entry.get().strip()
                stock = stock_entry.get().strip()
                proveedor = proveedor_entry.get().strip()
                precio = precio_entry.get().strip()
                status_val = status_entry.get().strip()
                marca = marca_entry.get().strip()
                descripcion = descripcion_entry.get().strip()

                # Validaciones
                if not nombre:
                    messagebox.showerror("Error", "El nombre del producto es obligatorio")
                    nombre_entry.focus_set()
                    return

                if not proveedor:
                    messagebox.showerror("Error", "El proveedor es obligatorio")
                    proveedor_entry.focus_set()
                    return

                # Validar números
                try:
                    stock = int(stock) if stock else 0
                    precio = int(precio) if precio else 0
                    status_val = int(status_val) if status_val else 1
                except ValueError:
                    messagebox.showerror("Error", "Stock, Precio y Status deben ser números enteros")
                    return

                if stock < 0:
                    messagebox.showerror("Error", "El stock no puede ser negativo")
                    stock_entry.focus_set()
                    return

                if precio < 0:
                    messagebox.showerror("Error", "El precio no puede ser negativo")
                    precio_entry.focus_set()
                    return

                # Mostrar mensaje de procesamiento
                add_window.config(cursor="watch")
                btn_guardar.config(state="disabled")
                btn_cancelar.config(state="disabled")
                add_window.update()

                # Intentar agregar el producto
                exito, mensaje = agregar_producto(nombre, stock, proveedor, precio, status_val, marca, descripcion)
                
                if exito:
                    messagebox.showinfo("Éxito", mensaje)
                    add_window.destroy()
                    self.ver_productos()
                else:
                    messagebox.showerror("Error", mensaje)
                    
            except Exception as e:
                messagebox.showerror("Error", f"Error inesperado: {e}")
            finally:
                add_window.config(cursor="")
                btn_guardar.config(state="normal")
                btn_cancelar.config(state="normal")

        btn_frame = tk.Frame(main_frame)
        btn_frame.pack(pady=20)

        btn_guardar = tk.Button(btn_frame, text="Guardar", command=guardar, 
                               bg="green", fg="white", font=("Arial", 10), width=10)
        btn_guardar.pack(side=tk.LEFT, padx=10)

        btn_cancelar = tk.Button(btn_frame, text="Cancelar", command=add_window.destroy, 
                                bg="red", fg="white", font=("Arial", 10), width=10)
        btn_cancelar.pack(side=tk.LEFT, padx=10)

        # Bind Enter key para guardar
        add_window.bind('<Return>', lambda event: guardar())

    def ver_productos(self):
        try:
            for row in self.tree.get_children():
                self.tree.delete(row)
            
            productos = ver_productos()
            if productos:
                for p in productos:
                    # Asegurar que todos los valores sean strings
                    valores = [str(val) if val is not None else "" for val in p]
                    self.tree.insert("", tk.END, values=valores)
            else:
                print("No se encontraron productos o hubo un error")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar productos: {e}")

    def actualizar_producto(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un producto")
            return

        item = seleccion[0]
        datos = self.tree.item(item, 'values')

        update_window = tk.Toplevel(self.root)
        update_window.title("Actualizar Producto")
        update_window.geometry("400x500")
        
        # Centrar ventana de manera compatible
        self.centrar_ventana(update_window)
        update_window.grab_set()

        main_frame = tk.Frame(update_window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        tk.Label(main_frame, text="Nombre del Producto:*", font=("Arial", 10, "bold")).pack(anchor="w", pady=(5,2))
        nombre_entry = tk.Entry(main_frame, width=40, font=("Arial", 10))
        nombre_entry.insert(0, datos[1] if datos[1] else "")
        nombre_entry.pack(fill="x", pady=(0,10))

        tk.Label(main_frame, text="Stock:*", font=("Arial", 10, "bold")).pack(anchor="w", pady=(5,2))
        stock_entry = tk.Entry(main_frame, width=40, font=("Arial", 10))
        stock_entry.insert(0, datos[2] if datos[2] else "0")
        stock_entry.pack(fill="x", pady=(0,10))

        tk.Label(main_frame, text="Proveedor:*", font=("Arial", 10, "bold")).pack(anchor="w", pady=(5,2))
        proveedor_entry = tk.Entry(main_frame, width=40, font=("Arial", 10))
        proveedor_entry.insert(0, datos[3] if datos[3] else "")
        proveedor_entry.pack(fill="x", pady=(0,10))

        tk.Label(main_frame, text="Precio:*", font=("Arial", 10, "bold")).pack(anchor="w", pady=(5,2))
        precio_entry = tk.Entry(main_frame, width=40, font=("Arial", 10))
        precio_entry.insert(0, datos[4] if datos[4] else "0")
        precio_entry.pack(fill="x", pady=(0,10))

        tk.Label(main_frame, text="Status (0=Inactivo, 1=Activo):", font=("Arial", 10, "bold")).pack(anchor="w", pady=(5,2))
        status_entry = tk.Entry(main_frame, width=40, font=("Arial", 10))
        status_entry.insert(0, datos[5] if datos[5] else "1")
        status_entry.pack(fill="x", pady=(0,10))

        tk.Label(main_frame, text="Marca:", font=("Arial", 10)).pack(anchor="w", pady=(5,2))
        marca_entry = tk.Entry(main_frame, width=40, font=("Arial", 10))
        marca_entry.insert(0, datos[6] if datos[6] else "")
        marca_entry.pack(fill="x", pady=(0,10))

        tk.Label(main_frame, text="Descripción:", font=("Arial", 10)).pack(anchor="w", pady=(5,2))
        descripcion_entry = tk.Entry(main_frame, width=40, font=("Arial", 10))
        descripcion_entry.insert(0, datos[7] if datos[7] else "")
        descripcion_entry.pack(fill="x", pady=(0,10))

        def guardar_cambios():
            try:
                nombre = nombre_entry.get().strip()
                stock = stock_entry.get().strip()
                proveedor = proveedor_entry.get().strip()
                precio = precio_entry.get().strip()
                status_val = status_entry.get().strip()
                marca = marca_entry.get().strip()
                descripcion = descripcion_entry.get().strip()

                if not nombre or not proveedor:
                    messagebox.showerror("Error", "Nombre y proveedor son obligatorios")
                    return

                try:
                    stock = int(stock) if stock else 0
                    precio = int(precio) if precio else 0
                    status_val = int(status_val) if status_val else 1
                except ValueError:
                    messagebox.showerror("Error", "Stock, Precio y Status deben ser números enteros")
                    return

                update_window.config(cursor="watch")
                btn_guardar.config(state="disabled")
                btn_cancelar.config(state="disabled")
                update_window.update()

                exito, mensaje = actualizar_producto(datos[0], nombre, stock, proveedor, precio, status_val, marca, descripcion)
                
                if exito:
                    messagebox.showinfo("Éxito", mensaje)
                    update_window.destroy()
                    self.ver_productos()
                else:
                    messagebox.showerror("Error", mensaje)
                    
            except Exception as e:
                messagebox.showerror("Error", f"Error inesperado: {e}")
            finally:
                update_window.config(cursor="")
                btn_guardar.config(state="normal")
                btn_cancelar.config(state="normal")

        btn_frame = tk.Frame(main_frame)
        btn_frame.pack(pady=20)

        btn_guardar = tk.Button(btn_frame, text="Guardar", command=guardar_cambios, 
                               bg="green", fg="white", font=("Arial", 10), width=10)
        btn_guardar.pack(side=tk.LEFT, padx=10)

        btn_cancelar = tk.Button(btn_frame, text="Cancelar", command=update_window.destroy, 
                                bg="red", fg="white", font=("Arial", 10), width=10)
        btn_cancelar.pack(side=tk.LEFT, padx=10)

        update_window.bind('<Return>', lambda event: guardar_cambios())

    def eliminar_producto(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un producto")
            return

        item = seleccion[0]
        datos = self.tree.item(item, 'values')

        if messagebox.askyesno("Confirmar", f"¿Eliminar producto '{datos[1]}'?"):
            exito, mensaje = eliminar_producto(datos[0])
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.ver_productos()
            else:
                messagebox.showerror("Error", mensaje)

    def volver_dashboard(self):
        self.root.destroy()
        if NAVIGATION_AVAILABLE:
            volver_dashboard()
        else:
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
                try:
                    python = sys.executable
                    login_path = os.path.join(current_dir, "login_view.py")
                    if os.path.exists(login_path):
                        subprocess.Popen([python, login_path])
                except Exception as e:
                    print(f"Error cerrando sesión: {e}")

if __name__ == "__main__":
    app = ProductsApp()