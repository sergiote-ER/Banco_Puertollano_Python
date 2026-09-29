from datetime import datetime as dt
import os
import re

archivo_log = dt.now().strftime("%Y-%m-%d")

class Movimiento:
    def __init__(self, cantidad: float, tipo_operacion: str, tipo_cuenta: str):
        self.cantidad = cantidad
        self.tipo_operacion = tipo_operacion.capitalize()
        self.tipo_cuenta = tipo_cuenta.capitalize()

    def __str__(self):
        return f"{self.tipo_operacion} de {self.cantidad:.2f}€ en {self.tipo_cuenta}"

class Cliente:
    def __init__(self, numeroCliente: str):
        self.numero_cliente = numeroCliente
        self.saldo_cuenta = 0.0
        self.saldo_deposito = 0.0
        self.movimientos = []

    def cargar_datos_fichero(self) -> bool:
        nombreFicheroCliente = f"{self.numero_cliente}.txt"
        #Comprueba si el archivo existe realmente o no, si no existe manda un false, si existe pues no pasa por ahí evidentemente
        if not os.path.exists(nombreFicheroCliente):
            mensaje = f"ERROR: El fichero '{nombreFicheroCliente}' para el cliente {self.numero_cliente} no existe."
            print(f"\n{mensaje}")
            registrarLog(mensaje)
            return False

        try:
            with open(nombreFicheroCliente, "r", encoding="utf-8") as file:
                #Leemos to do el contenido y tokenizamos separando por espacios o saltos de línea
                contenido = file.read()
                tokens = contenido.split()
                for token in tokens:
                    token = token.strip()
                    if not token:
                        continue
                    #Formato esperado: Monto;Operacion;Cuenta;
                    partes = [p for p in token.split(";") if p]
                    if len(partes) < 3:
                        continue
                    monto = float(partes[0])
                    operacion = partes[1].strip()
                    cuenta = partes[2].strip()
                    movimiento = Movimiento(monto, operacion, cuenta)
                    self.movimientos.append(movimiento)
                    # Actualizar los saldos
                    if cuenta.lower() == "cuenta":
                        if operacion.lower() == "ingreso":
                            self.saldo_cuenta += monto
                        elif operacion.lower() == "retirada":
                            self.saldo_cuenta -= monto
                    elif cuenta.lower() == "deposito":
                        if operacion.lower() == "ingreso":
                            self.saldo_deposito += monto
                        elif operacion.lower() == "retirada":
                            self.saldo_deposito -= monto

            mensajeExito = f"ÉXITO: Se cargaron {len(self.movimientos)} movimientos para el cliente {self.numero_cliente} desde '{nombreFicheroCliente}'."
            print(f"\n{mensajeExito}")
            registrarLog(mensajeExito)
            return True

        except Exception as e:
            mensajeError = f"ERROR: Ocurrió una excepción al procesar '{nombreFicheroCliente}': {e}"
            print(f"\n{mensajeError}")
            registrarLog(mensajeError)
            return False

    def mostrar_resumen(self):
        print("\n=================================================")
        print(f" Resume de cuentas - cliente: {self.numero_cliente}")
        print("=================================================")
        print(f"Saldo cuenta corriente: {float(self.saldo_cuenta)} €")
        print(f"Saldo depósito: {float(self.saldo_deposito)} €")
        print("--------------------------------------------------")
        print(f"Total movimientos: {len(self.movimientos)}")
        print("==================================================")




def pedirNumeroCliente() -> str:
    while True:
        numero = input("\nIngrese el número de cliente (6 dígitos, ej: 432344): ").strip()
        if re.fullmatch(r"\d{6}", numero):
            return numero

        mensaje = f"ADVERTENCIA: Entrada de número de cliente inválida ('{numero}'). Formato requerido: NNNNNN."
        print(" Formato incorrecto. Debe tener exactamente 6 dígitos numéricos.")
        registrarLog(mensaje)

def registrarLog(mensaje: str):
    tiempoExacto = dt.now().strftime("%Y-%m-%d %H:%M:%S")
    linea = f"[{tiempoExacto}] {mensaje}\n"
    try:
        with open(archivo_log, "a", encoding="utf-8") as f:
            f.write(linea)
    except Exception as e:
        print(f"Error al escribir en el log: {e}")

def menu():
    print("\n--------------------------------------------------------------")
    print("Banco Puertollano")
    print("--------------------------------------------------------------")
    print("1. Cargar datos cliente")
    print("2. Consultar cuenta y deposito")
    print("3. Salir")
    print("--------------------------------------------------------------")

opcion = int(input("Escoge una opcion: "))
while opcion != 0:
    pass

def main():
    registrarLog("INICIO: Aplicación Banco Puertollano 2026 iniciada.")
    clienteActual = None

    while True:
        try:
            menu()
            opcion = int(input("Escoge una opcion: "))
            match opcion:
                case 1:
                    numCliente = pedirNumeroCliente()
                    nuevoCliente = Cliente(numCliente)
                    if nuevoCliente.cargar_datos_fichero():
                        clienteActual = nuevoCliente
                    else:
                        print(" No se pudieron cargar los datos del cliente.")

                case 2:
                    if clienteActual is None:
                        mensaje = "ADVERTENCIA: Intento de consulta sin ningún cliente cargado previamente."
                        print("\n No hay ningún cliente cargado. Seleccione la Opción 1 primero.")
                        registrarLog(mensaje)
                    else:
                        clienteActual.mostrar_resumen()
                        registrarLog(f"CONSULTA: Datos consultados para el cliente {clienteActual.numero_cliente}.")
                case 3:
                    print("\nGracias por usar los servicios de Banco Puertollano 2026. ¡Hasta pronto!")
                    registrarLog("FIN: La aplicación finalizó correctamente por el usuario.")
                case _:
                    mensaje = f"ADVERTENCIA: Opción de menú no válida introducida ('{opcion}')."
                    print("\n Opción no válida. Por favor, introduzca 1, 2 o 3.")
                    registrarLog(mensaje)
        except Exception as e:
            # Captura cualquier error inesperado para evitar que el programa se detenga
            mensajeCritico = f"CRÍTICO: Excepción no controlada en el bucle principal: {e}"
            print("\n Ha ocurrido un error inesperado. Reintente por favor.")
            registrarLog(mensajeCritico)

if __name__ == "__main__":
    main()