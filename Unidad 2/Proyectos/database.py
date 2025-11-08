import mysql.connector
from mysql.connector import Error

def crear_conexion():
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            database='poo_proyecto_parcial2',
            user='root',
            password=''
        )
        
        if conexion.is_connected():
            print("Conexión con MySQL establecida")
            return conexion
        else:
            print("No se pudo conectar a MySQL")
            return None
            
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None