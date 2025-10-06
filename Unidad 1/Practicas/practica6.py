from abc import ABC, abstractmethod
from typing import List, Dict
from enum import Enum
import datetime

# =============================================
# PATRÓN OBSERVER: Sistema de Notificaciones
# =============================================

class TipoNotificacion(Enum):
    """Enum para los tipos de notificación disponibles"""
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"

class Observador(ABC):
    """Interfaz Observador del patrón Observer"""
    
    @abstractmethod
    def actualizar(self, producto: 'Producto', mensaje: str):
        """Método que se ejecuta cuando el sujeto notifica un cambio"""
        pass

class Cliente(Observador):
    """Cliente que observa productos específicos"""
    
    def __init__(self, nombre: str, email: str, telefono: str):
        self.nombre = nombre
        self.email = email
        self.telefono = telefono
        self.productos_observados = set()
    
    def suscribirse_a_producto(self, producto: 'Producto'):
        """El cliente se suscribe a un producto para recibir notificaciones"""
        producto.agregar_observador(self)
        self.productos_observados.add(producto.nombre)
        print(f"{self.nombre} se suscribió a notificaciones de {producto.nombre}")
    
    def desuscribirse_de_producto(self, producto: 'Producto'):
        """El cliente deja de recibir notificaciones de un producto"""
        producto.eliminar_observador(self)
        self.productos_observados.discard(producto.nombre)
        print(f"{self.nombre} se desuscribió de notificaciones de {producto.nombre}")
    
    def actualizar(self, producto: 'Producto', mensaje: str):
        """Método llamado cuando el producto cambia de estado"""
        print(f"Notificación para {self.nombre}: {mensaje}")
        # En un caso real, aquí se enviaría el email, SMS, etc.

class Sujeto(ABC):
    """Interfaz Sujeto del patrón Observer"""
    
    def __init__(self):
        self._observadores: List[Observador] = []
    
    def agregar_observador(self, observador: Observador):
        """Agrega un observador a la lista"""
        if observador not in self._observadores:
            self._observadores.append(observador)
    
    def eliminar_observador(self, observador: Observador):
        """Elimina un observador de la lista"""
        self._observadores.remove(observador)
    
    def notificar_observadores(self, mensaje: str):
        """Notifica a todos los observadores registrados"""
        for observador in self._observadores:
            observador.actualizar(self, mensaje)

# =============================================
# PATRÓN FACTORY: Creación de Notificaciones
# =============================================

class Notificacion(ABC):
    """Interfaz base para todas las notificaciones"""
    
    @abstractmethod
    def enviar(self, destinatario: str, mensaje: str):
        """Envía la notificación al destinatario"""
        pass

class NotificacionEmail(Notificacion):
    """Notificación por correo electrónico"""
    
    def enviar(self, destinatario: str, mensaje: str):
        print(f"📧 Enviando EMAIL a {destinatario}: {mensaje}")

class NotificacionSMS(Notificacion):
    """Notificación por mensaje de texto"""
    
    def enviar(self, destinatario: str, mensaje: str):
        print(f"📱 Enviando SMS a {destinatario}: {mensaje}")

class NotificacionPush(Notificacion):
    """Notificación push para aplicación móvil"""
    
    def enviar(self, destinatario: str, mensaje: str):
        print(f"🔔 Enviando PUSH a {destinatario}: {mensaje}")

class FabricaNotificaciones:
    """Factory para crear diferentes tipos de notificaciones"""
    
    @staticmethod
    def crear_notificacion(tipo: TipoNotificacion) -> Notificacion:
        """Método factory que crea notificaciones según el tipo"""
        if tipo == TipoNotificacion.EMAIL:
            return NotificacionEmail()
        elif tipo == TipoNotificacion.SMS:
            return NotificacionSMS()
        elif tipo == TipoNotificacion.PUSH:
            return NotificacionPush()
        else:
            raise ValueError(f"Tipo de notificación no soportado: {tipo}")

# =============================================
# CLASES DEL DOMINIO: Productos y Ferretería
# =============================================

class Producto(Sujeto):
    """Producto de la ferretería que puede ser observado"""
    
    def __init__(self, nombre: str, categoria: str, precio: float, stock: int = 0):
        super().__init__()
        self.nombre = nombre
        self.categoria = categoria
        self.precio = precio
        self._stock = stock
        self.fecha_ultima_actualizacion = datetime.datetime.now()
    
    @property
    def stock(self) -> int:
        return self._stock
    
    @stock.setter
    def stock(self, nuevo_stock: int):
        """Setter que notifica a los observadores cuando cambia el stock"""
        stock_anterior = self._stock
        self._stock = nuevo_stock
        self.fecha_ultima_actualizacion = datetime.datetime.now()
        
        # Notificar cambios importantes
        if stock_anterior == 0 and nuevo_stock > 0:
            mensaje = f"✅ {self.nombre} ahora está disponible! Stock: {nuevo_stock}"
            self.notificar_observadores(mensaje)
        elif nuevo_stock == 0:
            mensaje = f"❌ {self.nombre} se ha agotado"
            self.notificar_observadores(mensaje)
        elif nuevo_stock < 5 and stock_anterior >= 5:
            mensaje = f"⚠️ {self.nombre} tiene stock bajo: {nuevo_stock} unidades"
            self.notificar_observadores(mensaje)
    
    def __str__(self):
        return f"{self.nombre} - ${self.precio} - Stock: {self.stock}"

class Ferreteria:
    """Sistema principal de la ferretería"""
    
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.productos: Dict[str, Producto] = {}
        self.clientes: List[Cliente] = []
        self.fabrica_notificaciones = FabricaNotificaciones()
    
    def agregar_producto(self, producto: Producto):
        """Agrega un producto al inventario de la ferretería"""
        self.productos[producto.nombre] = producto
        print(f"Producto agregado: {producto.nombre}")
    
    def registrar_cliente(self, cliente: Cliente):
        """Registra un nuevo cliente en el sistema"""
        self.clientes.append(cliente)
        print(f"Cliente registrado: {cliente.nombre}")
    
    def actualizar_stock(self, nombre_producto: str, nuevo_stock: int):
        """Actualiza el stock de un producto y notifica a los observadores"""
        if nombre_producto in self.productos:
            self.productos[nombre_producto].stock = nuevo_stock
        else:
            print(f"Producto no encontrado: {nombre_producto}")
    
    def enviar_promocion(self, tipo_notificacion: TipoNotificacion, mensaje: str):
        """Envía una promoción a todos los clientes usando el patrón Factory"""
        notificacion = self.fabrica_notificaciones.crear_notificacion(tipo_notificacion)
        
        for cliente in self.clientes:
            if tipo_notificacion == TipoNotificacion.EMAIL:
                notificacion.enviar(cliente.email, mensaje)
            elif tipo_notificacion == TipoNotificacion.SMS:
                notificacion.enviar(cliente.telefono, mensaje)
            elif tipo_notificacion == TipoNotificacion.PUSH:
                notificacion.enviar(cliente.nombre, mensaje)

# =============================================
# EJEMPLO DE USO: Simulación del Sistema
# =============================================

def main():
    """Función principal que demuestra el uso de los patrones"""
    print("🏪 SISTEMA DE FERRETERÍA 'EL MARTILLO FELIZ'")
    print("=" * 50)
    
    # Crear la ferretería
    ferreteria = Ferreteria("El Martillo Feliz")
    
    # Crear productos
    martillo = Producto("Martillo Professional", "Herramientas", 25.99, 0)
    tornillos = Producto("Tornillos Acero 2\"", "Fijaciones", 8.50, 10)
    pintura = Producto("Pintura Blanca 4L", "Pinturas", 45.75, 3)
    
    ferreteria.agregar_producto(martillo)
    ferreteria.agregar_producto(tornillos)
    ferreteria.agregar_producto(pintura)
    
    print("\n" + "-" * 50)
    
    # Crear clientes
    cliente1 = Cliente("Juan Pérez", "juan@email.com", "+123456789")
    cliente2 = Cliente("María García", "maria@email.com", "+987654321")
    cliente3 = Cliente("Carlos López", "carlos@email.com", "+555555555")
    
    ferreteria.registrar_cliente(cliente1)
    ferreteria.registrar_cliente(cliente2)
    ferreteria.registrar_cliente(cliente3)
    
    print("\n" + "-" * 50)
    
    # Los clientes se suscriben a productos
    print("\n📋 SUSCRIPCIONES DE CLIENTES:")
    cliente1.suscribirse_a_producto(martillo)  # Juan quiere saber cuando haya martillos
    cliente2.suscribirse_a_producto(martillo)  # María también quiere martillos
    cliente3.suscribirse_a_producto(pintura)   # Carlos quiere pintura
    
    print("\n" + "-" * 50)
    
    # Simular cambios en el stock
    print("\n🔄 ACTUALIZACIONES DE STOCK:")
    
    print("\n1. Llegan martillos al almacén:")
    ferreteria.actualizar_stock("Martillo Professional", 15)  # Notifica a Juan y María
    
    print("\n2. Stock de pintura baja:")
    ferreteria.actualizar_stock("Pintura Blanca 4L", 2)  # Notifica a Carlos
    
    print("\n3. Se agotan los tornillos:")
    ferreteria.actualizar_stock("Tornillos Acero 2\"", 0)  # No hay observadores
    
    print("\n4. Carlos se suscribe a tornillos y llegan nuevos:")
    cliente3.suscribirse_a_producto(tornillos)
    ferreteria.actualizar_stock("Tornillos Acero 2\"", 20)  # Notifica a Carlos
    
    print("\n" + "-" * 50)
    
    # Envío de promociones usando el patrón Factory
    print("\n🎯 CAMPAÑAS DE MARKETING (Patrón Factory):")
    
    print("\nPromoción por Email:")
    ferreteria.enviar_promocion(
        TipoNotificacion.EMAIL, 
        "¡Oferta especial! 20% de descuento en herramientas este fin de semana"
    )
    
    print("\nPromoción por SMS:")
    ferreteria.enviar_promocion(
        TipoNotificacion.SMS,
        "Ferreteria El Martillo: Lleva 3x2 en pinturas hasta domingo"
    )
    
    print("\nPromoción por Push:")
    ferreteria.enviar_promocion(
        TipoNotificacion.PUSH,
        "¡Nuevos productos disponibles! Visita nuestra app"
    )
    
    print("\n" + "-" * 50)
    
    # Mostrar estado final
    print("\n📊 ESTADO FINAL DEL SISTEMA:")
    for producto in ferreteria.productos.values():
        print(f"  - {producto}")
    
    print(f"\nClientes registrados: {len(ferreteria.clientes)}")
    for cliente in ferreteria.clientes:
        print(f"  - {cliente.nombre}: Suscrito a {len(cliente.productos_observados)} productos")

if __name__ == "__main__":
    main()