from database import crear_conexion

def ver_usuarios():
    conexion = crear_conexion()
    if not conexion:
        return []
    
    try:
        cursor = conexion.cursor()
        # CORREGIDO: Solo las columnas que existen
        cursor.execute("SELECT id, username, nombre FROM usuarios")
        resultado = cursor.fetchall()
        return resultado
    except Exception as e:
        print(f"Error al obtener usuarios: {e}")
        return []
    finally:
        if conexion:
            conexion.close()

def agregar_usuario(username, password, nombre=None):
    conexion = crear_conexion()
    
    if not conexion:
        return False
    
    try:
        cursor = conexion.cursor()
        # CORREGIDO: Solo las columnas que existen
        cursor.execute("INSERT INTO usuarios (username, password, nombre) VALUES (%s, %s, %s)", 
                      (username, password, nombre))
        conexion.commit()
        print(f"Usuario '{username}' agregado exitosamente")
        return True
        
    except Exception as e:
        print(f" Error al crear usuario: {e}")
        return False
    finally:
        if conexion:
            conexion.close()

def actualizar_usuario(id_usuario, username, password=None, nombre=None):
    conexion = crear_conexion()
    
    if not conexion:
        return False
    
    try:
        cursor = conexion.cursor()
        if password:  # Si se proporciona nueva contraseña
            cursor.execute("UPDATE usuarios SET username = %s, password = %s, nombre = %s WHERE id = %s", 
                          (username, password, nombre, id_usuario))
        else:  # Si no se cambia la contraseña
            cursor.execute("UPDATE usuarios SET username = %s, nombre = %s WHERE id = %s", 
                          (username, nombre, id_usuario))
        
        conexion.commit()
        print(f"Usuario ID {id_usuario} actualizado exitosamente")
        return True
        
    except Exception as e:
        print(f" Error al actualizar usuario: {e}")
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
        cursor.execute("DELETE FROM usuarios WHERE id = %s", (id_usuario,))
        conexion.commit()
        print(f" Usuario ID {id_usuario} eliminado exitosamente")
        return True
        
    except Exception as e:
        print(f" Error al eliminar usuario: {e}")
        return False
    finally:
        if conexion:
            conexion.close()

def buscar_usuario_por_id(id_usuario):
    conexion = crear_conexion()
    
    if not conexion:
        return None
    
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE id = %s", (id_usuario,))
        resultado = cursor.fetchone()
        return resultado
        
    except Exception as e:
        print(f" Error al buscar usuario: {e}")
        return None
    finally:
        if conexion:
            conexion.close()

def probar_funciones():
    print(" Probando funciones de usuarios...")
    
    print("\n Usuarios existentes:")
    usuarios = ver_usuarios()
    for usuario in usuarios:
        print(f"   ID: {usuario[0]}, Username: {usuario[1]}, Nombre: {usuario[2]}")
    
    if usuarios:
        print(f"\n Buscando usuario ID {usuarios[0][0]}:")
        usuario = buscar_usuario_por_id(usuarios[0][0])
        if usuario:
            print(f"   Encontrado: {usuario}")

if __name__ == "__main__":
    probar_funciones()