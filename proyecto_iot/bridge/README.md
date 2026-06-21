# Bridge MQTT ↔ Firebase — Hidroponía IoT

## Descripción
Puente Python que suscribe tópicos MQTT del broker Mosquitto y sincroniza los datos en Firebase Realtime Database en tiempo real.

## Requisitos
- Python 3.9+
- Docker + Docker Compose
- Proyecto en Firebase con Realtime Database habilitado

## Configuración rápida

1. **Copia el archivo de variables de entorno:**
   ```bash
   cp .env.example .env
   ```

2. **Edita `.env`** con tu URL de Firebase y la ruta al JSON de credenciales de tu cuenta de servicio.

3. **Descarga las credenciales Firebase:**  
   Firebase Console → Configuración del proyecto → Cuentas de servicio → Generar nueva clave privada  
   Guarda el archivo como `bridge/firebase-credentials.json`

## Ejecución

```bash
# 1. Levantar broker MQTT
docker-compose up -d

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Arrancar el bridge
python bridge.py
```

## Tópicos MQTT

| Tópico | QoS | Dirección | Descripción |
|--------|-----|-----------|-------------|
| `escom/iot/hidroponia/sensores/temperatura` | 0 | Sensor → Bridge | °C del DHT22 |
| `escom/iot/hidroponia/sensores/humedad` | 0 | Sensor → Bridge | % HR del DHT22 |
| `escom/iot/hidroponia/sensores/nivel_agua` | 1 | Sensor → Bridge | cm del HC-SR04 |
| `escom/iot/hidroponia/actuadores/bomba` | 2 | Bridge → Actuador | ON / OFF |

## Estructura del proyecto

```
proyecto_iot/
├── docker-compose.yml
├── mosquitto/
│   └── config/
│       └── mosquitto.conf
└── bridge/
    ├── bridge.py
    ├── requirements.txt
    ├── .env.example
    └── README.md
```
