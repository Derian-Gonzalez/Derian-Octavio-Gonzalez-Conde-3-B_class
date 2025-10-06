#Practica3 introduccion al polimorfismo 
#simular un sistema de cobro con multiples
#opciones de pago 

class pago_tarjeta: 
    def procesar_pago(self, cantidad):
        return f"procesando el pago de ${cantidad} con tarjeta"
    
class transferencia:
    def procesar_pago(self, cantidad): 
        return f"procesando el pago de ${cantidad} con transferencia"
    
class deposito:  
    def procesar_pago(self, cantidad): 
        return f"procesando el pago de ${cantidad} con deposito" 
    

class paypal:
    def procesar_pago(self, cantidad): 
        return f"procesando el pago de ${cantidad} con paypal"
    

#instancia
#metodos_pago = [pago_tarjeta(), transferencia(), deposito(), paypal()]

#for m in metodos_pago:
    #print(m.procesar_pago(500))



#Actividad 
# Crear una instancia para que aparezcan diferentes montos en los metodos de pago 
# instancias con montos diferentes
metodos_pago = [
    (pago_tarjeta(), 500),
    (transferencia(), 1200),
    (deposito(), 800),
    (paypal(), 300)
]

for metodo, monto in metodos_pago:
    print(metodo.procesar_pago(monto))

#Actividad 2, aplicar otro caso de pilimorfismo, con contextos diferentes

class NotificacionCorreo:
    def enviar_notificacion(self, mensaje):
        return f" Enviando correo con mensaje: '{mensaje}'"

class NotificacionSMS:
    def enviar_notificacion(self, mensaje):
        return f"Enviando SMS con mensaje: '{mensaje}'"

class NotificacionWhatsApp:
    def enviar_notificacion(self, mensaje):
        return f" Enviando WhatsApp con mensaje: '{mensaje}'"

class NotificacionPush:
    def enviar_notificacion(self, mensaje):
        return f" Enviando notificación Push con mensaje: '{mensaje}'"

notificaciones = [
    (NotificacionCorreo(), "Tu pedido fue confirmado"),
    (NotificacionSMS(), "Tu paquete ha sido enviado"),
    (NotificacionWhatsApp(), "Tu pedido está por llegar"),
    (NotificacionPush(), "Tu paquete fue entregado")
]

for canal, mensaje in notificaciones:
    print(canal.enviar_notificacion(mensaje))
