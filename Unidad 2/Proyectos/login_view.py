# login_view.py
import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os

# Configurar rutas
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

try:
    from navigation import volver_dashboard, abrir_gestion_usuarios, abrir_gestion_productos
    NAVIGATION_AVAILABLE = True
except ImportError as e:
    print(f"Navigation no disponible: {e}")
    NAVIGATION_AVAILABLE = False

class LoginApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Login - Sistema de Gestión")
        self.root.geometry("400x350")
        self.root.resizable(False, False)
        
        # Centrar ventana
        self.root.eval('tk::PlaceWindow . center')
        
        self.crear_login()
        self.root.mainloop()
    
    def crear_login(self):
        frame_principal = tk.Frame(self.root)
        frame_principal.pack(expand=True, fill="both", padx=50, pady=50)
        
        # Título
        tk.Label(frame_principal, text="INICIAR SESIÓN", 
                font=("Arial", 18, "bold"), fg="darkblue").pack(pady=30)
        
        # Frame para campos de entrada
        frame_campos = tk.Frame(frame_principal)
        frame_campos.pack(fill="x", pady=10)
        
        # Usuario
        lbl_usuario = tk.Label(frame_campos, text="Usuario:", font=("Arial", 12))
        lbl_usuario.grid(row=0, column=0, sticky="w", pady=(0,15))
        
        self.entry_usuario = tk.Entry(frame_campos, font=("Arial", 12), width=25)
        self.entry_usuario.grid(row=0, column=1, padx=(10,0), pady=(0,15), sticky="ew")
        
        # Contraseña
        lbl_password = tk.Label(frame_campos, text="Contraseña:", font=("Arial", 12))
        lbl_password.grid(row=1, column=0, sticky="w", pady=(0,15))
        
        self.entry_password = tk.Entry(frame_campos, font=("Arial", 12), width=25, show="*")
        self.entry_password.grid(row=1, column=1, padx=(10,0), pady=(0,15), sticky="ew")
        
        # Configurar columnas para que se expandan
        frame_campos.columnconfigure(1, weight=1)
        
        # Frame para botones
        frame_botones = tk.Frame(frame_principal)
        frame_botones.pack(pady=20)
        
        # Botón Ingresar - PRINCIPAL
        btn_ingresar = tk.Button(frame_botones, text="🔐 Ingresar", 
                            command=self.iniciar_sesion,
                            bg="#27ae60", fg="white", font=("Arial", 12, "bold"),
                            width=12, height=1)
        btn_ingresar.pack(side=tk.LEFT, padx=10)
        
        # Botón Cancelar
        btn_cancelar = tk.Button(frame_botones, text="❌ Cancelar", 
                            command=self.cancelar,
                            bg="#e74c3c", fg="white", font=("Arial", 10),
                            width=10, height=1)
        btn_cancelar.pack(side=tk.LEFT, padx=10)
        
        # Información (solo en desarrollo)
        lbl_info = tk.Label(frame_principal, text="Usuario demo: admin / Contraseña: admin",
                font=("Arial", 9), fg="gray")
        lbl_info.pack(pady=10)
        
        # Enfocar el campo de usuario al iniciar
        self.entry_usuario.focus_set()
        
        # Bind Enter key para iniciar sesión
        self.entry_password.bind('<Return>', lambda event: self.iniciar_sesion())
    
    def iniciar_sesion(self):
        username = self.entry_usuario.get().strip()
        password = self.entry_password.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Por favor complete todos los campos")
            self.entry_usuario.focus_set()
            return
        
        # Validación simple
        if username == "admin" and password == "admin":
            messagebox.showinfo("Login Exitoso", f"Bienvenido, {username}!")
            self.root.destroy()
            
            # Usar navegación confiable
            if NAVIGATION_AVAILABLE:
                volver_dashboard()
            else:
                # Fallback
                try:
                    python = sys.executable
                    dashboard_path = os.path.join(current_dir, "dashboard.py")
                    if os.path.exists(dashboard_path):
                        subprocess.Popen([python, dashboard_path])
                    else:
                        messagebox.showerror("Error", "No se pudo encontrar el dashboard")
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo abrir el dashboard: {e}")
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")
            self.limpiar_campos()
    
    def limpiar_campos(self):
        """Limpia los campos y coloca el foco en usuario"""
        self.entry_password.delete(0, tk.END)
        self.entry_usuario.delete(0, tk.END)
        self.entry_usuario.focus_set()
    
    def cancelar(self):
        if messagebox.askyesno("Salir", "¿Está seguro de que desea salir del sistema?"):
            self.root.destroy()

if __name__ == "__main__":
    app = LoginApp()