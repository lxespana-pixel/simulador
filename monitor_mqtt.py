import paho.mqtt.client as mqtt
import json

BROKER_MQTT = "broker.hivemq.com"
PUERTO = 1883
TEMA = "granja/ecuador/jaula1/sensores"

# Esta función se ejecuta automáticamente cuando nos conectamos con éxito al broker
def on_connect(client, userdata, flags, rc, properties=None):
    print(f" Conectado exitosamente al Broker MQTT.")
    print(f" Suscribiéndose al tema: '{TEMA}'...")
    client.subscribe(TEMA)
    print("Esperando mensajes en tiempo real...\n")

# Esta función se ejecuta automáticamente cada vez que llega un mensaje nuevo al tema
def on_message(client, userdata, msg):
    try:
        # Decodificamos el mensaje que llegó por el aire
        payload_decodificado = msg.payload.decode()
        datos = json.loads(payload_decodificado)
        
        print(f" [MENSAJE RECIBIDO POR MQTT]")
        print(f"   Tema: {msg.topic}")
        print(f"   Temp: {datos.get('temperatura')} °C")
        print(f"   Hum: {datos.get('humedad')} %")
        print(f"   Amoníaco: {datos.get('amoníaco')} ppm")
        print("   -------------------------------------------------")
    except Exception as e:
        print(f"Error al procesar mensaje: {e}")

# Configurar el cliente MQTT (Soporta paho-mqtt v1 y v2)
try:
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
except AttributeError:
    client = mqtt.Client()

# Asignamos las funciones que creamos arriba a los eventos de la librería
client.on_connect = on_connect
client.on_message = on_message

print("Iniciando receptor de datos...")
client.connect(BROKER_MQTT, PUERTO, 60)

# Mantiene el script corriendo indefinidamente escuchando la red
client.loop_forever()