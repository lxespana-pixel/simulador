import requests
import time
from datetime import datetime, timezone, timedelta

# Gateway
URL_API = "https://8pkac0pg3d.execute-api.us-east-2.amazonaws.com/lecturas"

# zona horaria de (UTC-5) conversión de hora
ZONA_ECUADOR = timezone(timedelta(hours=-5))

# Variable para rastrear la última lectura que ya mostramos en pantalla
ultimo_timestamp_procesado = 0

print("=========================================================")
print("     MONITOR EN TIEMPO REAL - JAULA DE POLLITOS (AWS)    ")
print("=========================================================")
print("Escuchando nuevas lecturas desde la nube... \n[Presiona Ctrl + C para detener]\n")

while True:
    try:
        # petición GET API
        respuesta = requests.get(URL_API)
        
        if respuesta.status_code == 200:
            lecturas = respuesta.json()
            
            if lecturas:
                # lecturas de la más antigua a la más nueva
                # imprime en orden cronológico correcto
                lecturas_ordenadas = sorted(lecturas, key=lambda x: x.get('fecha_hora', 0))
                
                for lectura in lecturas_ordenadas:
                    timestamp = lectura.get('fecha_hora', 0)
                    
                    # procesamos si es una lectura que no hemos mostrado antes
                    if timestamp > ultimo_timestamp_procesado:
                        
                        # Convertimos el tiempo Unix a la hora real de Ecuador
                        fecha_hora_local = datetime.fromtimestamp(timestamp, tz=ZONA_ECUADOR)
                        fecha_formateada = fecha_hora_local.strftime('%d/%m/%Y a las %H:%M:%S')
                        
                        print(f" [NUEVO REGISTRO DETECTADO] - {fecha_formateada}")
                        print(f"   Identificador de Jaula: {int(lectura.get('id_jaula', 1))}")
                        print("   -------------------------------------------------")
                        
                        # Extrae y formatea cada uno de los sensores
                        datos_sensores = lectura.get('datos_sensores', [])
                        for sensor in datos_sensores:
                            nombre = sensor.get('nombre', 'Sensor')
                            valor = sensor.get('valor', 0.0)
                            unidad = sensor.get('unidad', '')
                            
                            print(f"    {nombre:15} : {valor:.2f} {unidad}")
                            
                        print("=========================================================\n")
                        
                        # Actualiza nuestro rastreador para no repetir esta lectura
                        ultimo_timestamp_procesado = timestamp
                        
        else:
            print(f"[API ERROR] No se pudo consultar. Código: {respuesta.status_code}")
            
    except Exception as e:
        print(f"[CONEXIÓN ERROR] Error al conectar con AWS: {e}")
        
    # Espera 5 segundos antes de volver a verificar si hay nuevos datos en la nube
    time.sleep(5)