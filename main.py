
from machine import Pin, ADC, PWM
from umqtt.simple import MQTTClient
import network, time


import config


ldr = ADC(Pin(34)); ldr.atten(ADC.ATTN_11DB)

r = PWM(Pin(25), 1000)
g = PWM(Pin(26), 1000)
b = PWM(Pin(27), 1000)


umbral = 30 
brillo = 100 
color = (255, 255, 255) 
modo = "auto" 
ultimo_nivel = -100 


def aplicar(encendida):
    if encendida:
        k = brillo / 100
    else:
        k = 0
    r.duty(int(color[0] / 255 * 1023 * k))
    g.duty(int(color[1] / 255 * 1023 * k))
    b.duty(int(color[2] / 255 * 1023 * k))

def leer_nivel():
    promedio = sum(ldr.read() for _ in range(10)) / 10
    return 100 - round(promedio / 4095 * 100)

def on_msg(topic, msg):
    global umbral, brillo, color, modo
    t = topic.decode() 
    m = msg.decode()
    if t.endswith("umbral"): 
        umbral = int(m)
    elif t.endswith("brillo"): 
        brillo = int(m)
    elif t.endswith("color"):
        h = m.lstrip("#")
        color = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    elif t.endswith("modo"): 
        modo = m

def conectar_mqtt():
    cliente = MQTTClient(
        config.MQTT_CLIENT_ID,
        config.MQTT_SERVER,
        port = config.MQTT_PORT,
        user = config.MQTT_USER,
        password = config.MQTT_PASSWORD,
        ssl = config.MQTT_SSL,
    )
    cliente.set_callback(on_msg)
    cliente.connect()
    for t in (config.TOPIC_UMBRAL, config.TOPIC_BRILLO,
              config.TOPIC_COLOR, config.TOPIC_MODO):
        cliente.subscribe(t)
    print("MQTT conectado a", config.MQTT_SERVER)
    return cliente

client = conectar_mqtt()

while True:
    client.check_msg()
    nivel = leer_nivel()
    if abs(nivel - ultimo_nivel) >= 2:
        client.publish(config.TOPIC_NIVEL, str(nivel))
        ultimo_nivel = nivel
    if modo == "auto":  
        aplicar(nivel < umbral)
    elif modo == "on": 
        aplicar(True)
    else: 
        aplicar(False)
    time.sleep_ms(200)
