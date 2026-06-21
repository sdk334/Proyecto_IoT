"""
Diagnóstico del bridge — prueba cada componente por separado.
Ejecutar desde la carpeta bridge/:
    python test_bridge.py
"""

import os, sys, time
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

MQTT_BROKER    = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT      = int(os.getenv("MQTT_PORT", 1883))
FIREBASE_DB_URL = os.getenv("FIREBASE_DATABASE_URL")
FIREBASE_CREDS  = os.getenv("FIREBASE_CREDENTIALS_PATH", "./firebase-credentials.json")

SEP = "=" * 50

# ── TEST 1: MQTT ──────────────────────────────────────
def test_mqtt():
    print(f"\n{SEP}")
    print("TEST 1 — Conexión MQTT")
    print(f"  Broker : {MQTT_BROKER}:{MQTT_PORT}")
    print(SEP)

    import paho.mqtt.client as mqtt_lib

    connected = [False]
    received  = [None]

    def on_connect(client, userdata, flags, rc, *args):
        rc_val = rc if isinstance(rc, int) else rc.value
        if rc_val == 0:
            print("  [OK] Conectado al broker")
            connected[0] = True
            client.subscribe("test/hidroponia")
            client.publish("test/hidroponia", "hola", qos=0)
        else:
            print(f"  [ERROR] rc={rc_val}")

    def on_message(client, userdata, msg):
        received[0] = msg.payload.decode()
        print(f"  [OK] Mensaje recibido: {received[0]}")

    try:
        client = mqtt_lib.Client(
            mqtt_lib.CallbackAPIVersion.VERSION1,
            client_id="test_client"
        )
    except AttributeError:
        client = mqtt_lib.Client(client_id="test_client")

    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, keepalive=5)

    client.loop_start()
    time.sleep(3)
    client.loop_stop()
    client.disconnect()

    if not connected[0]:
        print("  [FALLO] No se pudo conectar al broker MQTT")
        print("  -> Verifica que Docker y Mosquitto estén corriendo")
        print("  -> Ejecuta: docker ps")
        return False
    if received[0] is None:
        print("  [ADVERTENCIA] Conectado pero no recibió el mensaje de prueba")
    return connected[0]


# ── TEST 2: Firebase ──────────────────────────────────
def test_firebase():
    print(f"\n{SEP}")
    print("TEST 2 — Firebase Realtime Database")
    print(f"  URL: {FIREBASE_DB_URL}")
    print(SEP)

    if not FIREBASE_DB_URL:
        print("  [ERROR] FIREBASE_DATABASE_URL no está en .env")
        return False

    if not os.path.exists(FIREBASE_CREDS):
        print(f"  [ERROR] No existe: {FIREBASE_CREDS}")
        return False

    try:
        import firebase_admin
        from firebase_admin import credentials, db as fdb

        # Evitar "app ya inicializada" si se corre varias veces
        try:
            firebase_admin.get_app()
        except ValueError:
            cred = credentials.Certificate(FIREBASE_CREDS)
            firebase_admin.initialize_app(cred, {"databaseURL": FIREBASE_DB_URL})

        ts = datetime.utcnow().isoformat() + "Z"
        fdb.reference("test/ping").set({"valor": "pong", "timestamp": ts})
        val = fdb.reference("test/ping").get()
        print(f"  [OK] Escritura y lectura exitosas: {val}")
        # Limpiar nodo de prueba
        fdb.reference("test").delete()
        return True
    except Exception as e:
        print(f"  [ERROR] {e}")
        print("  -> Verifica firebase-credentials.json y FIREBASE_DATABASE_URL")
        print("  -> Verifica reglas de Firebase (deben permitir read/write)")
        return False


# ── TEST 3: Publicar sensor de prueba ─────────────────
def test_publish():
    print(f"\n{SEP}")
    print("TEST 3 — Publicar datos de sensor de prueba")
    print(SEP)

    import paho.mqtt.client as mqtt_lib

    published = [False]

    def on_connect(client, userdata, flags, rc, *args):
        rc_val = rc if isinstance(rc, int) else rc.value
        if rc_val == 0:
            r1 = client.publish("escom/iot/hidroponia/sensores/temperatura", "23.5", qos=0)
            r2 = client.publish("escom/iot/hidroponia/sensores/humedad",     "61.0", qos=0)
            r3 = client.publish("escom/iot/hidroponia/sensores/nivel_agua",  "19.2", qos=1)
            print(f"  Temperatura publicada (rc={r1.rc})")
            print(f"  Humedad     publicada (rc={r2.rc})")
            print(f"  Nivel agua  publicada (rc={r3.rc})")
            published[0] = True

    try:
        client = mqtt_lib.Client(
            mqtt_lib.CallbackAPIVersion.VERSION1,
            client_id="test_publisher"
        )
    except AttributeError:
        client = mqtt_lib.Client(client_id="test_publisher")

    client.on_connect = on_connect
    client.connect(MQTT_BROKER, MQTT_PORT, keepalive=5)
    client.loop_start()
    time.sleep(2)
    client.loop_stop()
    client.disconnect()

    if published[0]:
        print("  [OK] Si bridge.py está corriendo, los datos ya están en Firebase")
    else:
        print("  [FALLO] No se pudo publicar (broker no disponible)")
    return published[0]


# ── Main ──────────────────────────────────────────────
if __name__ == "__main__":
    print("\nDIAGNÓSTICO BRIDGE — Hidroponía IoT")
    print(SEP)

    r1 = test_mqtt()
    r2 = test_firebase()
    r3 = test_publish() if r1 else False

    print(f"\n{SEP}")
    print("RESUMEN")
    print(f"  MQTT broker  : {'OK' if r1 else 'FALLO'}")
    print(f"  Firebase     : {'OK' if r2 else 'FALLO'}")
    print(f"  Publicación  : {'OK' if r3 else 'FALLO (o no probado)'}")
    print(SEP)

    if not r1:
        print("\nPASOS PARA MQTT:")
        print("  1. Ejecuta Docker Desktop")
        print("  2. En la carpeta proyecto_iot: docker compose up -d")
        print("  3. Verifica: docker ps  (debe aparecer mosquitto)")

    if not r2:
        print("\nPASOS PARA FIREBASE:")
        print("  1. Ve a https://console.firebase.google.com")
        print("  2. Realtime Database -> Reglas")
        print('  3. Cambia a: { "rules": { ".read": true, ".write": true } }')
        print("  4. Verifica que firebase-credentials.json está en bridge/")
