#Practica 5. Patrones de diseño

class Logger:
    #Creamos un atributo de clase donde guarda la unica instancia
    _instancia = None 

# new es el metodo que controla la creacion del objeto antes de init.
#  Sirve para asegurarnos que solo exista una unica instancia de la clase Logger
    def _new_(cls, *args, **kwargs):
        #args es un argumento posicional que permite recibir multiples 
        # parametros.
        #**kwargs permite cualquier cantidad de parametros.


        #Valida si existe o no la instancia aun:
        if cls._instancia is None:
            cls.instancia = super().new_(cls)  #Creamos instancia de logger
            #Agregando un atributo "archivo" que apunta a un archivo fisico
            #"a" significa append = Todo lo que se escriba se agraga al final del archivo.
            cls._instancia.archivo = open("app.log", "a")
        return cls._instancia # Devolvemos siempre la misma instancia.
    
    def log(self, mensaje):
        #Simulando un registro de logs.
         self.archivo.write(mensaje + "\n")
         self.archivo.flush() #Metodo Para guardar en el disco. 

logger1=Logger() #Creamos la primera y unica instancia.
logger2=Logger() #Devolver la misma instancia, sin crear una nueva.

logger1.log("Inicio de sesion en la aplicacion")
logger2.log("El usuario se autentico")

#Comprobar que son el mismo objeto en memoria.
print(logger1 is logger2) #Devuelve true o false.

# Actividad de la practica
 
class Presidente:
    _instancia = None
    def _new_(cls, nombre):
        if cls._instancia is None:
            cls.instancia = super().new_(cls)
            cls._instancia.nombre = nombre
            cls._instancia.historial = []
        return cls._instancia
    
    def accion(self, accion):
        evento = f"{self.nombre} {accion}"
        self.historial.append(evento)
        print(evento)
#Varios presidentes intentan tomar el poder
p1 = Presidente("AMLO")
p2 = Presidente("Peña Nieto")
p3 = Presidente("Fox")
        
# Todos apuntan al mismo presidente
p1.accion("Firmo decreto")
p2.accion("Visito España")
p3.accion("aprobo un presupuesto")

print("\nHistorial del presidente")
print(p1.historial)

#Validacion de singleton
print(p1 is p2 is p3) #True o false

# 1.¿Que pasaria si eliminamos la verificacion if cls._instancia is None en el metodo new?
# Se generaría una nueva instancia distinta. Eso rompería el concepto de Singleton, porque
# ya no habría una sola instancia compartida, 
# sino varias copias independientes en memoria.

# 2. Que significa el "True" en p1 is p2 is p3 en el contexto del metodo sigleton?
# Significa que los tres objetos son el mismo en memoria y comparten datos.

# 3. Es buena idea usar Singleton para todo lo que sea global? Menciona un ejemplo donde no seria recomendable.
# No es recomendable usarlo para todo lo global, ejemplo: sesiones de usuarios o entidades que deban ser independientes.