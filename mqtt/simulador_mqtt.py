import paho.mqtt.client as mqtt
import time
import random
import json


BROKER_MQTT = "broker.hivemq.com"
PUERTO = 1883
TEMA = "granja/ecuador/jaula1/sensores"


try:
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
except AttributeError:
    client = mqtt.Client() 

print("Conectando al Broker MQTT público...")
client.connect(BROKER_MQTT, PUERTO, 60)

print(f"Simulador MQTT listo. Publicando datos en el tema: '{TEMA}' cada 5 segundos.\n")

while True:
    try:
        temp = round(random.uniform(18.0, 24.0), 1)
        hum = round(random.uniform(50.0, 70.0), 1)
        amon = round(random.uniform(0.5, 2.0), 2)
        
        paquete_datos = {
            "id_jaula": 1,
            "temperatura": temp,
            "humedad": hum,
            "amoníaco": amon
        }
        
        mensaje_json = json.dumps(paquete_datos)
        client.publish(TEMA, mensaje_json)
        
        print(f" [MQTT ENVIADO] Tema: '{TEMA}' | Datos: {mensaje_json}")
        
    except Exception as e:
        print(f"[ERROR] No se pudo enviar por MQTT: {e}")
        
    time.sleep(5)