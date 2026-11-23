# Se ejecuta al encender el ESP32, antes que main.py para realizar la conexcion WiFi
# Importamos librerias utilizadas
import network
import time

# Importo el archivo config.py
import config

# Funcion para conectar a la red WiFi, con el parametro timeout
def conectar_wifi(timeout=40):
    # Creo una variable volatil para controlar la placa WiFi del ESP32 y la declaro en modo cliente
    wlan = network.WLAN(network.STA_IF)
    # Activo la placa WiFi
    wlan.active(True)

    # Si ya estaba conectada, devuelvo la conexion
    if wlan.isconnected():
        # El comando wlan.ifconfig() devuelve una tupla con la IP, máscara de red, puerta de enlace y DNS
        print("Ya conectado:", wlan.ifconfig())
        return wlan

    # Caso contrario, intento conectarme a la red WiFi con los datos de config.py
    print("Conectando a", config.WIFI_SSID, "...")
    # Realizo el intento de conexion
    wlan.connect(config.WIFI_SSID, config.WIFI_PASSWORD)

    # Almaceno el tiempo de inicio
    inicio = time.time()
    # Realiza un bucle while hasta que se conecte o supere el tiempo de espera
    while not wlan.isconnected():
        # Si supera el tiempo establecido en timeout, devuelve error
        if time.time() - inicio > timeout: 
            print("No se pudo conectar al WiFi (timeout)")
            return None
        # Espera 500 ms antes de volver a consultar la conexion
        time.sleep(0.5)

    print("WiFi conectado:", wlan.ifconfig())
    return wlan

# Creo una variable global con el resultado de la conexion WiFi
wlan = conectar_wifi()