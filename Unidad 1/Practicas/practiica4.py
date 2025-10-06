#1- crea una clase de ticket con los siguientes atributos
#id, tipo (por ejemplo: software, prueba),prioridad(alta, media, baja), estado(por defecto, pendiente)
#crea dos tickets de ejemplo y mostrarlos por pantalla 

class ticket:
    def __init__ (self, id, tipo, prioridad, estado="pendiente"):
        self.id = id
        self.tipo = tipo
        self.prioridad = prioridad
        self.estado = estado

    def mostrar_ticket(self):
        print(f"ticket id: {self.id}")    
        print(f"tipo: {self.tipo}")    
        print(f"prioridad: {self.prioridad}")    
        print(f"estado: {self.estado}")    
        print(f"-" * 30)

ticket1 = ticket(1, "software", "alta")
ticket2 = ticket(2, "prueba", "media")

ticket1.mostrar_ticket()
ticket2.mostrar_ticket()

#clase empleado
#A) Crear una clase de empleadio con atributo nombre 
#B) Crear metodo trabajar_en_ticket(self, ticket) que imprima " El empleado nombre revisa el ticket id" 

class Empleado:
    # A) Crear una clase de empleado con atributo nombre
    def __init__(self, nombre):
        self.nombre = nombre
    
    # B) Crear método trabajar_en_ticket(self, ticket) que imprima "El empleado nombre revisa el ticket id"
    def trabajar_en_ticket(self, ticket):
        print(f"El empleado {self.nombre} revisa el ticket {ticket.id}")

class Ticket:
    def __init__(self, id, tipo, prioridad, estado="pendiente"):
        self.id = id
        self.tipo = tipo
        self.prioridad = prioridad
        self.estado = estado

    def mostrar_ticket(self):
        print(f"Ticket id: {self.id}")    
        print(f"Tipo: {self.tipo}")    
        print(f"Prioridad: {self.prioridad}")    
        print(f"Estado: {self.estado}")    
        print("-" * 30)

# Crear tickets
ticket1 = Ticket(1, "software", "alta")
ticket2 = Ticket(2, "prueba", "media")

# Crear empleados
empleado1 = Empleado("Carlos Rodríguez")
empleado2 = Empleado("Ana Martínez")

# Mostrar información de tickets
ticket1.mostrar_ticket()
ticket2.mostrar_ticket()

# Empleados trabajando en tickets
empleado1.trabajar_en_ticket(ticket1)
empleado2.trabajar_en_ticket(ticket2)

# Crear clase desarroladoer que herede de empleado y sobreescriba el metodo trabajar_enticket
#solo se puede resolver tickets de tipo software validacion
#si lo hace cambia el estaDO A RESUELTO y muestar un mensaje


class Desarrollador(Empleado):
    def trabajar_ticket(self,ticket):
        if ticket.tipo == "software":
            ticket.estado == "resuelto"
            print(f" El ticket {ticket.id} fue resuelto por {self.nombre}")
        else:
            print("Este tipo de empleado no puede resolver el ticket")    

#crear clase tester que solo pueda resolver tickets de tipo prueba ( condicion)
class tester(Empleado):
    def trabajar_ticket(self,ticket):
        if ticket.tipo == "prueba":
            ticket.estado == "resuelto"
            print(f" El ticket {ticket.id} fue resuelto por {self.nombre}")
        else:
            print("Este tipo de empleado no puede resolver el ticket")    

#crea una clase project_manajer que asigne ticketrs 
#crea la clase de project_manajer que herede empleado 


class project_manager(Empleado):
    def asignar_ticket(self, ticket, empleado):
        print(f"{self.nombre} asigno el ticket {ticket.id}, al empleado {empleado.nombre}")
        empleado.trabajar_ticket(ticket)

#Crear ticket y empleados 
ticket1 = Ticket(1, "software", "alta")
ticket2 = Ticket(2, "prueba", "media")

developer1 = Desarrollador("gustambo")
tester1= tester ("pablo")
pm1= project_manager ("susana")
pm1.asignar_ticket(ticket1,developer1) 

#Parte adicional 
# agregar un menu con while y con if que permita:
#1 crear un ticket 
#2 ver tickets 
#3 asignar tickets 
#4 salir del programa 

# Menú 

tickets = [ticket1, ticket2]

while True:
    print("\n--- MENÚ ---")
    print("1. Crear un ticket")
    print("2. Ver tickets")
    print("3. Asignar tickets")
    print("4. Salir")

    opcion = input("Selecciona una opción: ")

    if opcion == "1":
        id_ticket = len(tickets) + 1
        tipo = input("Tipo de ticket: ")
        prioridad = input("Prioridad: ")
        nuevo_ticket = Ticket(id_ticket, tipo, prioridad)
        tickets.append(nuevo_ticket)
        print("Ticket creado.")
    elif opcion == "2":
        for t in tickets:
            t.mostrar_ticket()
    elif opcion == "3":
        id_ticket = int(input("ID del ticket a asignar: "))
        for t in tickets:
            if t.id == id_ticket:
                empleado = input("Asignar a (developer/tester): ").lower()
                if empleado == "developer":
                    developer1.trabajar_en_ticket(t)
                elif empleado == "tester":
                    tester1.trabajar_en_ticket(t)
                else:
                    print("Empleado no válido.")
                break
        else:
            print("Ticket no encontrado.")
    elif opcion == "4":
        print("Saliendo...")
        break
    else:
        print("Opción no válida.")