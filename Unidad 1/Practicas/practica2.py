#Practica 2 atributos publicos y privados 

class persona:
    def __init__(self, nombre, edad,):
        self.nombre= nombre
        self.edad=edad
        self._cuenta= None #Atributo privado
    def presentarse(self):
        print(f"hola mi nombre es {self.nombre} y mi edad es {self.edad}")

    def cumplir_anios(self):
        self.edad +=1
        print(f"Esta persona cumplio {self.edad} años") 

    def asignar_cuenta(self, cuenta):
        self.__cuenta = cuenta 
        print(f"{self.nombre} ahora tiene una cuenta bancaria")  

    def consultar_saldo(self):
        if self.__cuenta:
            print(f" El saldo de {self.nombre} es ${self.__cuenta.mostrar_saldo()}")
        else:
            print(f"{self.nombre} aun no tiene cuenta bancaria")           

persona1= persona("Miguel",20)
persona1.presentarse()
persona1
#Se creo un objeto o instancia de la clase 
print(persona1.nombre)
print(persona1.edad)
#Acceso a los valores de los atributos publicos 

class cuenta_bancaria:
    def __init__(self,num_cuenta, saldo):
        self.num_cuenta = num_cuenta
        self.__saldo = saldo 

    def mostrar_saldo(self):
        return self.__saldo    

    def depositar(self, cantidad):
        if cantidad > 0:
            self.__saldo += cantidad
            print(f" Se deposito la cantidad de $ {cantidad} a la cuenta, el nuevo saldo de la cuenta es: {self.__saldo}")
        else: 
            print(" Ingresa una cantidad valida")

    def retirar(self, retiro, dinero, cantidad):
        if retiro <= self.__saldo:
            self.__saldo -= cantidad
            print(f" Se retiro  la cantidad de $ {cantidad} a la cuenta,")
        else: 
            print(" Ingresa una cantidad menor a la de su saldo ")



persona1= persona("Miguel",20)
cuenta1= cuenta_bancaria("001", 500)
persona1.asignar_cuenta(cuenta1)
persona1.consultar_saldo()
#Se creo un objeto o instancia de la clase 
print(persona1.nombre)
print(persona1.edad)
#Acceso a los valores de los atributos publicos 
