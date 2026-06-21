"""
Bridge MQTT <-> Firebase Realtime Database
Proyecto: Hidroponía IoT - ESCOM

Flujo sensores : ESP32 --> MQTT --> bridge --> Firebase --> Dashboard
Flujo bomba    : Dashboard --> Firebase --> bridge --> MQTT --> ESP32
"""

import os
import logging
import threading
from datetime import datetime
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, db

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
log = logging.getLogger(__name__)

# --- Configuración ---
MQTT_BROKER     = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT       = int(os.getenv("MQTT_PORT", 1883))
MQTT_CLIENT_ID  = os.getenv("MQTT_CLIENT_ID", "bridge_hidroponia")
FIREBASE_DB_URL = os.getenv("FIREBASE_DATABASE_URL")
FIREBASE_CREDS  = os.getenv("FIREBASE_CREDENTIALS_PATH", "./firebase-credentials.json")

TOPIC_TEMP   = os.getenv("TOPIC_TEMPERATURA",  "escom/iot/hidroponia/sensores/temperatura")
TOPIC_HUM    = os.getenv("TOPIC_HUMEDAD",       "escom/iot/hidroponia/sensores/humedad")
TOPIC_NIVEL  = os.getenv("TOPIC_NIVEL_AGUA",    "escom/iot/hidroponia/sensores/nivel_agua")
TOPIC_BOMBA  = os.getenv("TOPIC_BOMBA",         "escom/iot/hidroponia/actuadores/bomba")

# Solo sensores se suscriben vía MQTT (la bomba llega por Firebase)
SENSOR_MQTT_TOPICS = [
    (TOPIC_TEMP,  0),
    (TOPIC_HUM,   0),
    (TOPIC_NIVEL, 1),
]

SENSOR_TOPICS = {TOPIC_TEMP, TOPIC_HUM, TOPIC_NIVEL}

# Evita loop: registra el último valor que el bridge publicó a MQTT
_last_mqtt_pump = None

# --- Firebase ---
def init_firebase():
    cred = credentials.Certificate(FIREBASE_CREDS)
    firebase_admin.initialize_app(cred, {"databaseURL": FIREBASE_DB_URL})
    log.info("Firebase inicializado: %s", FIREBASE_DB_URL)

def firebase_path(topic: str) -> str:
    parts = topic.split("/")
    return "/".join(parts[-2:])

def write_to_firebase(topic: str, payload: str):
    path = firebase_path(topic)
    data = {"valor": payload, "timestamp": datetime.utcnow().isoformat() + "Z"}
    db.reference(path).set(data)
    log.info("Firebase [%s] <- %s", path, payload)
    if topic in SENSOR_TOPICS:
        sensor_name = path.split("/")[-1]
        db.reference(f"historial/{sensor_name}").push(data)

# --- Firebase listener: bomba Dashboard -> MQTT -> ESP32 ---
def start_firebase_pump_listener(mqtt_client):
    """Escucha cambios en actuadores/bomba y los reenvía por MQTT al ESP32."""

    def on_pump_change(event):
        global _last_mqtt_pump
        data = event.data
        if data is None:
            return
        valor = data.get("valor") if isinstance(data, dict) else str(data)
        if valor not in ("ON", "OFF"):
            return
        # Evitar publicar si ya enviamos ese valor (previene loops)
        if valor == _last_mqtt_pump:
            log.debug("Bomba: valor ya publicado (%s), ignorando", valor)
            return
        _last_mqtt_pump = valor
        mqtt_client.publish(TOPIC_BOMBA, valor, qos=2, retain=True)
        log.info("Bomba Firebase->MQTT: %s", valor)

    db.reference("actuadores/bomba").listen(on_pump_change)
    log.info("Firebase listener activo: actuadores/bomba")

# --- MQTT Callbacks ---
def on_connect(client, userdata, flags, rc, *args):
    rc_val = rc if isinstance(rc, int) else rc.value
    if rc_val == 0:
        log.info("Conectado al broker MQTT %s:%s", MQTT_BROKER, MQTT_PORT)
        client.subscribe(SENSOR_MQTT_TOPICS)
        for topic, qos in SENSOR_MQTT_TOPICS:
            log.info("  Suscrito: %s  (QoS %s)", topic, qos)
        # Iniciar listener de Firebase en hilo separado (requiere cliente MQTT ya conectado)
        threading.Thread(
            target=start_firebase_pump_listener,
            args=(client,),
            daemon=True
        ).start()
    else:
        log.error("Error conexión MQTT, rc=%s", rc_val)

def on_disconnect(client, userdata, rc, *args):
    log.warning("Desconectado del broker (rc=%s)", rc)

def on_message(client, userdata, msg):
    topic   = msg.topic
    payload = msg.payload.decode("utf-8").strip()
    log.info("MQTT [%s] QoS=%s -> %s", topic, msg.qos, payload)
    try:
        write_to_firebase(topic, payload)
    except Exception as e:
        log.error("Error escribiendo en Firebase: %s", e)

# --- Main ---
def main():
    init_firebase()

    import paho.mqtt.client as mqtt_lib

    try:
        client = mqtt_lib.Client(
            mqtt_lib.CallbackAPIVersion.VERSION1,
            client_id=MQTT_CLIENT_ID
        )
        log.info("paho-mqtt 2.x detectado")
    except AttributeError:
        client = mqtt_lib.Client(client_id=MQTT_CLIENT_ID)
        log.info("paho-mqtt 1.x detectado")

    client.on_connect    = on_connect
    client.on_disconnect = on_disconnect
    client.on_message    = on_message

    log.info("Conectando a broker %s:%s ...", MQTT_BROKER, MQTT_PORT)
    client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
    client.loop_forever()

if __name__ == "__main__":
    main()
