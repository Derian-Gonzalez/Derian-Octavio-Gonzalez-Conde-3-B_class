#practica 1 clases, objetos y atributos
# una clase es practicamente una plantilla o un molde que define como sera un objeto
class persona:
    def __init__(self, nombre, edad,):
        self.nombre= nombre
        self.edad=edad

    def estudiar(self):
        print(f"hola mi nombre es {self.nombre} y mi edad es {self.edad}")

    def cumplir_anios(self):
        self.edad +=1
        print(f"Esta persona cumplio {self.edad} años")      

#un objeto es una estancia creada a partir de una clase 
estudiante1 = persona("derian", 19)
estudiante2 = persona("william", 19)
estudiante1.cumplir_anios()

#paso 1, agrega un metodo cumplir_anios(), que aumente en 1 la edad

#instancia: cada objeto creado de una clase es una instancia, podemos tener varias instancias que coexistan con sus 
# propios datos, objeto es igual a una instancia de la clase y cada vez que se crea un objeto o clase se obtiene 
# una instancia independiente, cada instancia tiene sus propios datos aunque vengan de la misma clase 

# abstraccion 
# representar solo lo importante del mundo real, ocultando detalles inecesarios.

class automovil:
    def __init__(self, marca):
        self.marca=marca

    def arrancar(self):
        print(f"{self.marca} arranco")    

#crear un objeto auto y asignar una marca 
auto=automovil("nissan")
auto.arrancar()
#abstraccion nos sentramos solo en lo que nos importa, accion que es arrancar el automovil, ocultando detalles internos 
# como motor, transmission, tipo de combustible. 
# enfoque solo en la accion del objeto 
# objetivo es hacer el codigo mad limpio y facil de usar. 

# ejercicio 1. 2 
#crea una clase mascotas
# agregar minimo 4 atributos 
# definir al menos 4 metodos diferentes  
class mascotas:
    def __init__(self, raza, edad, vacunas, sexo):
        self.raza=raza
        self.edad=edad
        self.vacunas=vacunas
        self.sexo=sexo

    def identificacion (self):
        raza=input(f"¿Cual es la raza de su mascota? : ")


    def años (self):
        edad=input(f"Edad del cachorro:")
        edad * 10 
        print(f"Su mascota tiene en años perrunos {self,edad}")

    def salud (self):
        print(f"¿")         











# crear 2 instancias de la clase 
#llamar los metodos y aplicar abstraccion  (agregar un atributo innecesario)