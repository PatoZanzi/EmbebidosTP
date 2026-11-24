import network
import time

import config

def conectar_wifi(timeout=40):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if wlan.isconnected():
        print("Ya conectado:", wlan.ifconfig())
        return wlan
    print("Conectando a", config.WIFI_SSID, "...")
    wlan.connect(config.WIFI_SSID, config.WIFI_PASSWORD)
    inicio = time.time()
    while not wlan.isconnected():
        if time.time() - inicio > timeout: 
            print("No se pudo conectar al WiFi (timeout)")
            return None
        time.sleep(0.5)
    print("WiFi conectado:", wlan.ifconfig())
    return wlan
wlan = conectar_wifi()
