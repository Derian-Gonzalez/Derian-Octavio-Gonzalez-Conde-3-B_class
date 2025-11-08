# dashboard.py
import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os

# Configurar rutas
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

try:
    from navigation import abrir_gestion_usuarios, abrir_gestion_productos, volver_login
    NAVIGATION_AVAILABLE = True
except ImportError as e:
    print(f"Navigation no disponible: {e}")
    NAVIGATION_AVAILABLE = False

class Dashboard:
    def __init__(self, username="admin"):
        self.username = username
        self.root = tk.Tk()
        self.root.title(f"Dashboard - Sistema de Gestión - Usuario: {username}")
        self.root.geometry("500x450")
        self.root.resizable(False, False)
        
        # Centrar ventana
        self.root.eval('tk::PlaceWindow . center')
        
        self.crear_dashboard()
        self.root.mainloop()
    
    def crear_dashboard(self):
        frame_principal = tk.Frame(self.root)
        frame_principal.pack(expand=True, fill="both", padx=50, pady=50)
        
        tk.Label(frame_principal, text="DASHBOARD PRINCIPAL", 
                font=("Arial", 20, "bold"), fg="darkblue").pack(pady=20)
        
        tk.Label(frame_principal, text=f"Bienvenido: {self.username}", 
                font=("Arial", 14, "bold"), fg="green").pack(pady=5)
        
        tk.Label(frame_principal, text="Panel de Control", 
                font=("Arial", 14, "bold")).pack(pady=10)
        
        frame_botones = tk.Frame(frame_principal)
        frame_botones.pack(pady=30)
        
        btn_usuarios = tk.Button(frame_botones, text="👥 Gestión de Usuarios", 
                               command=self.abrir_gestion_usuarios,
                               bg="#3498db", fg="white", font=("Arial", 12, "bold"),
                               width=20, height=2)
        btn_usuarios.pack(pady=15)
        
        btn_productos = tk.Button(frame_botones, text="📦 Gestión de Productos", 
                                command=self.abrir_gestion_productos,
                                bg="#2ecc71", fg="white", font=("Arial", 12, "bold"),
                                width=20, height=2)
        btn_productos.pack(pady=15)
        
        btn_salir = tk.Button(frame_botones, text="🚪 Cerrar Sesión", 
                            command=self.cerrar_sesion,
                            bg="#e74c3c", fg="white", font=("Arial", 10),
                            width=15, height=1)
        btn_salir.pack(pady=20)
        
        tk.Label(frame_principal, text="Seleccione el módulo que desea gestionar",
                font=("Arial", 10), fg="gray").pack(pady=10)
    
    def abrir_gestion_usuarios(self):
        self.root.destroy()
        if NAVIGATION_AVAILABLE:
            abrir_gestion_usuarios()
        else:
            # Fallback
            try:
                python = sys.executable
                user_view_path = os.path.join(current_dir, "user_view.py")
                if os.path.exists(user_view_path):
                    subprocess.Popen([python, user_view_path])
                else:
                    messagebox.showerror("Error", "No se pudo encontrar gestión de usuarios")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo abrir gestión de usuarios: {e}")
    
    def abrir_gestion_productos(self):
        self.root.destroy()
        if NAVIGATION_AVAILABLE:
            abrir_gestion_productos()
        else:
            # Fallback
            try:
                python = sys.executable
                products_view_path = os.path.join(current_dir, "products_view.py")
                if os.path.exists(products_view_path):
                    subprocess.Popen([python, products_view_path])
                else:
                    messagebox.showerror("Error", "No se pudo encontrar gestión de productos")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo abrir gestión de productos: {e}")
    
    def cerrar_sesion(self):
        if messagebox.askyesno("Cerrar Sesión", "¿Está seguro de que desea cerrar sesión?"):
            self.root.destroy()
            if NAVIGATION_AVAILABLE:
                volver_login()
            else:
                # Fallback
                try:
                    python = sys.executable
                    login_view_path = os.path.join(current_dir, "login_view.py")
                    if os.path.exists(login_view_path):
                        subprocess.Popen([python, login_view_path])
                except Exception as e:
                    print(f"Error al cerrar sesión: {e}")

if __name__ == "__main__":
    dashboard = Dashboard()