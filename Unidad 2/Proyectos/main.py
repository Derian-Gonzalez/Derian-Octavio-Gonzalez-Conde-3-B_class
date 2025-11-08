# main.py
import os
import sys

# Forzar la ruta al directorio actual para evitar problemas de rutas
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from login_view import LoginApp

if __name__ == "__main__":
    app = LoginApp()