from database import crear_conexion

def validar_credenciales(usuario, password):
    conexion = crear_conexion()
    
    if not conexion:
        return False

    cursor = conexion.cursor()  
    consulta = "SELECT * FROM usuarios WHERE username = %s AND password = %s"
    cursor.execute(consulta, (usuario, password))
    result = cursor.fetchone()     

    conexion.close()
    return bool(result)