
# cafetería.py
# Menú de cafetería con selección de productos

productos = ["latte", "capuchino", "americano"]
precios = [50, 70, 40]

# Función para calcular el total
def calcular_total(pedido, precios):
    total = 0
    for producto, cantidad in pedido.items():
        indice = productos.index(producto)
        total += cantidad * precios[indice]
    return total

# Función para imprimir el ticket
def imprimir_ticket(nombre, pedido, productos, precios):
    print("\n" + "=" * 40)
    print("           TICKET DE COMPRA")
    print("=" * 40)
    print(f"Cliente: {nombre}")
    print("-" * 40)
    print("Producto         Cantidad   Precio  Subtotal")
    print("-" * 40)
    
    total = 0
    for producto, cantidad in pedido.items():
        if cantidad > 0:
            indice = productos.index(producto)
            subtotal = cantidad * precios[indice]
            total += subtotal
            print(f"{producto:<12} {cantidad:>8}   ${precios[indice]:>5}   ${subtotal:>6}")
    
    print("-" * 40)
    print(f"TOTAL: ${total:>31}")
    print("=" * 40)
    print("¡Gracias por su compra!")

# Menú principal
print("Menú de cafetería - Bienvenido")
nombre = input("Ingresa tu nombre: ")

# Mostrar menú disponible
print("\nNuestro menú disponible:")
for i in range(len(productos)):
    print(f"{i+1}. {productos[i]} - ${precios[i]}")

pedido = {producto: 0 for producto in productos} 
# Preguntar por cada producto individualmente
for i in range(len(productos)):
    try:
        cantidad = int(input(f"\n¿Cuántos {productos[i]} desea ordenar? "))
        if cantidad >= 0:
            pedido[productos[i]] = cantidad
        else:
            print("Por favor ingrese una cantidad válida (número positivo).")
            pedido[productos[i]] = 0
    except ValueError:
        print("Por favor ingrese un número válido.")
        pedido[productos[i]] = 0

# Calcular total e imprimir ticket
total = calcular_total(pedido, precios)
imprimir_ticket(nombre, pedido, productos, precios)