# Script para controlar un LED RGB con un LDR y MQTT 
# Importo librerias utilizadas
from machine import Pin, ADC, PWM
from umqtt.simple import MQTTClient
import network, time
# Importo el archivo config.py y boot.py
import config

# Declaro los pines del ESP32 que se utilizaran para el LDR y el LED RGB
# Utilizo un pin que transforme un valor analogico a uno digital
ldr = ADC(Pin(34)); ldr.atten(ADC.ATTN_11DB)
# Utilizo una señal duty para controlar el brillo del led
# Realizo una frecuencia de 1000 ciclos por segundo para que el led permanezca encendido al ojo humano
r = PWM(Pin(25), 1000)
g = PWM(Pin(26), 1000)
b = PWM(Pin(27), 1000)

# Declaro e inicializo las variables globales que se utilizaran para controlar el LED RGB
umbral = 30 # Valor de referencia para encender o apagar el LED RGB
brillo = 100 # Valor de referencia para el brillo del LED RGB
color = (255, 255, 255) # Valor de referencia para el color del LED RGB
modo = "auto" # Valor de referencia para el modo de funcionamiento del LED RGB
ultimo_nivel = -100 # Valor de referencia para el nivel de luz leido por el LDR

# Funcion para aplicar los valores de brillo y color al LED RGB
def aplicar(encendida):
    # Si esta encendido modifico el brillo, sino lo dejo en 0
    if encendida:
        k = brillo / 100
    else:
        k = 0
    # Modifico los valores para rojo, azul y verde
    r.duty(int(color[0] / 255 * 1023 * k))
    g.duty(int(color[1] / 255 * 1023 * k))
    b.duty(int(color[2] / 255 * 1023 * k))

# Funcion para leer la luminosidad del ambiente
def leer_nivel():
    # Obtengo el valor promedio cada 10 lecturas para reducir ruido y oscilaciones de la resistencia fotosensible
    promedio = sum(ldr.read() for _ in range(10)) / 10
    # Transformo el valor analogico a uno digital
    return 100 - round(promedio / 4095 * 100)   # 0-100 %

# Funcion para modificar un valor (mediante protocolo MQTT)
def on_msg(topic, msg):
    # Utilizo las variables globales
    global umbral, brillo, color, modo
    # Creo variables para decodificar los paquetes de datos
    t = topic.decode() 
    m = msg.decode()
    # dependiendo del contenido entra en alguno de los condicionales para modificar un valor
    if t.endswith("umbral"): 
        umbral = int(m)
    elif t.endswith("brillo"): 
        brillo = int(m)
    elif t.endswith("color"):
        h = m.lstrip("#")
        # Transformo un dato hexadecimal (Ej: FF8800) en tres enteros del 0 al 255 cada 2 caracteres
        color = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    elif t.endswith("modo"): # condcional para modificar el modo de funcionamiento
        modo = m

# Funcion para conectarse al broker
def conectar_mqtt():
    # Creo una objeto que utilizo para realizar conexion con MQTT
    cliente = MQTTClient(
        config.MQTT_CLIENT_ID,
        config.MQTT_SERVER,
        port = config.MQTT_PORT,
        user = config.MQTT_USER,
        password = config.MQTT_PASSWORD,
        ssl = config.MQTT_SSL,
    )
    # Indico que Funcion va a recibir los mensajes
    cliente.set_callback(on_msg)
    # Realizo la conexion
    cliente.connect()
    # Me suscribo a los tópicos que controla el dashboard
    for t in (config.TOPIC_UMBRAL, config.TOPIC_BRILLO,
              config.TOPIC_COLOR, config.TOPIC_MODO):
        cliente.subscribe(t)
    print("MQTT conectado a", config.MQTT_SERVER)
    return cliente

# Creo una variable global que almacene al objeto cliente
client = conectar_mqtt()


# Bucle que revise si hay mensajes nuevos
while True:
    # Chequeo si el objeto client recibio informacion nueva
    client.check_msg()
    # Leo la luminosidad del ambiente
    nivel = leer_nivel()
    # Si la luminosidad cambia en 2 puntos (para evitar ruido y oscilaciones) se hace un publish
    if abs(nivel - ultimo_nivel) >= 2:
        # Realizo el publish y parseo a nivel en un string (cadena de texto)
        client.publish(config.TOPIC_NIVEL, str(nivel))
        ultimo_nivel = nivel
    # Si el modo es auto
    if modo == "auto":  
        # Enciende el RGB si la comparacion BOOLEANA da TRUE (cuando nivel es menor a umbral) 
        aplicar(nivel < umbral)
    # Si el modo es manual
    elif modo == "on": 
        aplicar(True)
    else: # Utilizo el modo off o cualquier otra palabra para apagar el led
        aplicar(False)
    # Cada 200 ms vuelve a hacer el bucle while 
    time.sleep_ms(200)