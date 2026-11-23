# Credenciales separadas del código principal para no exponerlas al compartir main.py

# --- WiFi (el ESP32 solo soporta redes de 2.4 GHz) ---
WIFI_SSID = "Wokwi-GUEST" 
WIFI_PASSWORD = ""

# --- Broker MQTT ---
# Utilizamos HiveMQ Cloud, un servicio de broker MQTT gratuito y administrado por la nube
# Utilizamos el puerto 8883 que cuenta con cifrado para proteger la informacion transmitida
# Se puede utilizar tambien el puerto 1883 sin cifrado pero a nivel de seguridad no es recomendable
MQTT_SERVER = "broker.hivemq.com" # URL de red que apunta a un servidor MQTT
MQTT_PORT = 1883 # Puerto de conexion con el servidor
MQTT_SSL = False # Condicion de activacion TLS (si fuera False no se cifraria la informacion)

MQTT_USER = None # Nombre de usuario para loguearse en el servidor MQTT
MQTT_PASSWORD = None # Contraseña para loguearse en el servidor MQTT
MQTT_CLIENT_ID = "esp32_luz_habitacion" # Identificador del ESP32 en el servidor MQTT

# --- Topicos ---
# Canales por donde se mueven los paquetes de datos
TOPIC_NIVEL = b"luz/nivel"      # ESP32 publica
TOPIC_UMBRAL = b"luz/umbral"    # ESP32 se suscribe
TOPIC_BRILLO = b"luz/brillo"    # ESP32 se suscribe
TOPIC_COLOR = b"luz/color"      # ESP32 se suscribe
TOPIC_MODO = b"luz/modo"        # ESP32 se suscribe