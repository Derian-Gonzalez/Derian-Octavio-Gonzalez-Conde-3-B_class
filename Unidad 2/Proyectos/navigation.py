# navigation.py
import subprocess
import sys
import os

def abrir_archivo(nombre_archivo):
    """Abre un archivo Python de manera confiable"""
    try:
        python = sys.executable
        script_dir = os.path.dirname(os.path.abspath(__file__))
        archivo_path = os.path.join(script_dir, nombre_archivo)
        
        print(f"Intentando abrir: {archivo_path}")  # Para debug
        
        if os.path.exists(archivo_path):
            subprocess.Popen([python, archivo_path])
            return True
        else:
            print(f"Error: No se encontró {archivo_path}")
            # Intentar con rutas alternativas
            alternativas = [
                nombre_archivo,
                f"./{nombre_archivo}",
                os.path.join(os.getcwd(), nombre_archivo)
            ]
            
            for alt_path in alternativas:
                if os.path.exists(alt_path):
                    subprocess.Popen([python, alt_path])
                    return True
            
            return False
    except Exception as e:
        print(f"Error navegando a {nombre_archivo}: {e}")
        return False

def volver_dashboard():
    """Vuelve al dashboard de manera confiable"""
    return abrir_archivo("dashboard.py")

def volver_login():
    """Vuelve al login de manera confiable"""
    return abrir_archivo("login_view.py")

def abrir_gestion_usuarios():
    """Abre gestión de usuarios"""
    return abrir_archivo("user_view.py")

def abrir_gestion_productos():
    """Abre gestión de productos"""
    return abrir_archivo("products_view.py")