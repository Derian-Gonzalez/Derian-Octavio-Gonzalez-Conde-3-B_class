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

def ver_productos():
    conexion = crear_conexion()
    if not conexion:
        return []
    
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT id_producto, nombre_producto, stock, proveedor, precio, status, marca, description FROM productos")
        resultado = cursor.fetchall()
        return resultado
    except Exception as e:
        print(f"Error al obtener productos: {e}")
        return []
    finally:
        if conexion:
            conexion.close()

def agregar_producto(nombre_producto, stock, proveedor, precio, marca=None, description=None):
    conexion = crear_conexion()
    
    if not conexion:
        return False
    
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO productos (nombre_producto, stock, proveedor, precio, marca, description) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (nombre_producto, stock, proveedor, precio, marca, description))
        conexion.commit()
        print(f"Producto '{nombre_producto}' agregado exitosamente")
        return True
        
    except Exception as e:
        print(f"Error al crear producto: {e}")
        return False
    finally:
        if conexion:
            conexion.close()

def actualizar_producto(id_producto, nombre_producto, stock, proveedor, precio, marca=None, description=None):
    conexion = crear_conexion()
    
    if not conexion:
        return False
    
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE productos 
            SET nombre_producto = %s, stock = %s, proveedor = %s, precio = %s, marca = %s, description = %s 
            WHERE id_producto = %s
        """, (nombre_producto, stock, proveedor, precio, marca, description, id_producto))
        conexion.commit()
        print(f"Producto ID {id_producto} actualizado exitosamente")
        return True
        
    except Exception as e:
        print(f"Error al actualizar producto: {e}")
        return False
    finally:
        if conexion:
            conexion.close()

def eliminar_producto(id_producto):
    conexion = crear_conexion()
    
    if not conexion:
        return False
    
    try:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM productos WHERE id_producto = %s", (id_producto,))
        conexion.commit()
        print(f"Producto ID {id_producto} eliminado exitosamente")
        return True
        
    except Exception as e:
        print(f"Error al eliminar producto: {e}")
        return False
    finally:
        if conexion:
            conexion.close()

def buscar_producto_por_id(id_producto):
    conexion = crear_conexion()
    
    if not conexion:
        return None
    
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM productos WHERE id_producto = %s", (id_producto,))
        resultado = cursor.fetchone()
        return resultado
        
    except Exception as e:
        print(f"Error al buscar producto: {e}")
        return None
    finally:
        if conexion:
            conexion.close()

def probar_funciones():
    print("Probando funciones de productos...")
    
    print("\nProductos existentes:")
    productos = ver_productos()
    for producto in productos:
        print(f"   ID: {producto[0]}, Nombre: {producto[1]}, Stock: {producto[2]}, Precio: {producto[4]}")
    
    if productos:
        print(f"\nBuscando producto ID {productos[0][0]}:")
        producto = buscar_producto_por_id(productos[0][0])
        if producto:
            print(f"   Encontrado: {producto}")

if __name__ == "__main__":
    probar_funciones()