WIFI_SSID = "Wokwi-GUEST" 
WIFI_PASSWORD = ""

MQTT_SERVER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_SSL = False

MQTT_USER = None
MQTT_PASSWORD = None
MQTT_CLIENT_ID = "esp32_luz_habitacion"

TOPIC_NIVEL = b"luz/nivel"      # ESP32 publica    
TOPIC_UMBRAL = b"luz/umbral"    # ESP32 se suscribe
TOPIC_BRILLO = b"luz/brillo"    # ESP32 se suscribe
TOPIC_COLOR = b"luz/color"      # ESP32 se suscribe
TOPIC_MODO = b"luz/modo"        # ESP32 se suscribe
