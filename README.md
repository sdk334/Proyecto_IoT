# Sistema de Monitoreo y Control IoT para Hidroponía

## 1. Descripción del Proyecto

Este proyecto implementa una arquitectura IoT para el monitoreo y control automatizado de un sistema hidropónico. Combina la eficiencia y ligereza del protocolo MQTT en la capa Edge con la sincronización en tiempo real de Firebase en la capa Cloud. Permite la lectura de sensores y el accionamiento de bombas de agua tanto desde una interfaz web como desde una aplicación móvil nativa (Android). Además, incorpora un **chat de IA (HydroBot)** que asiste al usuario resolviendo dudas sobre el funcionamiento del sistema y el cuidado del cultivo hidropónico.

![torre de hidroponia](/imagenes/torre_hidroponia.jpg)

## 2. Arquitectura del Sistema

La arquitectura se divide en tres capas interconectadas:

* **Capa Edge (Hardware y MQTT):** Microcontrolador ESP32 que publica datos de sensores simulados (temperatura, humedad, nivel de agua) y escucha comandos de actuadores a través de un Broker Eclipse Mosquitto 2.0 corriendo en Docker.
* **Capa Cloud e Integración (Firebase):** Un servicio puente (`bridge.py`) bidireccional que conecta el tráfico MQTT con Firebase Realtime Database. Persiste lecturas de sensores y propaga comandos de control (bomba) desde la nube hacia el ESP32.
* **Capa de Aplicación (Frontend):**
    * **Dashboard Web:** SPA desarrollada con React 18 + Vite 5, gráficas históricas con Recharts y tema oscuro con Tailwind CSS.
    * **Aplicación Móvil (HidroSync):** App nativa Android en Kotlin con Foreground Service, notificación persistente animada y control de bomba sin abrir la app.
    * **Chat de IA (HydroBot):** Asistente conversacional con RAG contextual integrado en la app móvil que inyecta los valores actuales de los sensores en cada consulta.

## 3. Tecnologías Utilizadas

| Componente | Tecnología |
| :--- | :--- |
| Microcontrolador | ESP32 DevKit V1 |
| Firmware | C/C++ (Framework Arduino) + PubSubClient |
| Broker MQTT | Eclipse Mosquitto 2.0 |
| Despliegue Broker | Docker + Docker Compose |
| Bridge Middleware | Python 3.11+ (paho-mqtt 1.6.1, firebase-admin 6.5.0) |
| Base de Datos | Firebase Realtime Database |
| Dashboard Web | React 18 + Vite 5 + Recharts + Tailwind CSS |
| App Móvil | Android (Kotlin), SDK mín. API 34, Firebase BOM 33.7.0 |
| Chat IA | Cohere API (modelo command-r) con RAG contextual |

## 4. Árbol de Tópicos MQTT

El sistema utiliza una estructura jerárquica de 5 niveles con niveles de QoS asignados según la criticidad del dato:

| Tópico | QoS | Descripción | Dirección |
| :--- | :---: | :--- | :---: |
| `escom/iot/hidroponia/sensores/temperatura` | 0 | Temperatura ambiente (°C) | ESP32 → Broker |
| `escom/iot/hidroponia/sensores/humedad` | 0 | Humedad relativa (%) | ESP32 → Broker |
| `escom/iot/hidroponia/sensores/nivel_agua` | 1 | Nivel del tanque (cm) | ESP32 → Broker |
| `escom/iot/hidroponia/actuadores/bomba` | 2 | Comando ON/OFF de la bomba | Firebase → Bridge → Broker → ESP32 |

> QoS 0 para telemetría frecuente (pérdida tolerable), QoS 1 para nivel de agua (at-least-once), QoS 2 para el actuador (exactly-once, crítico).

## 5. Estructura de la Base de Datos Firebase

```json
{
  "sensores": {
    "temperatura": { "valor": "23.5", "timestamp": "..." },
    "humedad":     { "valor": "61.4", "timestamp": "..." },
    "nivel_agua":  { "valor": "16.5", "timestamp": "..." }
  },
  "actuadores": {
    "bomba": { "valor": "ON", "timestamp": "..." }
  },
  "historial": {
    "temperatura": { "-Nxxx": { "valor": "23.5", "timestamp": "..." } },
    "humedad":     { "-Nxxx": { "valor": "61.4", "timestamp": "..." } },
    "nivel_agua":  { "-Nxxx": { "valor": "16.5", "timestamp": "..." } }
  }
}
```

## 6. Chat de IA — HydroBot

HydroBot es el asistente virtual integrado en la app Android. Usa la **API de Cohere (modelo command-r)** con un sistema de RAG contextual ligero: antes de cada consulta inyecta el estado actual de los sensores (temperatura, humedad, nivel de agua, estado de bomba) leído desde Firebase, permitiendo respuestas específicas al huerto del usuario.

Funciones principales:
* **Resolución de dudas** sobre el sistema y su configuración.
* **Interpretación de datos** en tiempo real (valores actuales inyectados automáticamente).
* **Recomendaciones** ante valores fuera de rango óptimo.
* Chips de preguntas frecuentes predefinidas para acceso rápido.

## 7. Requisitos Previos

* **Docker Desktop** instalado y en ejecución (para Mosquitto).
* **Python 3.11+** con pip.
* **Node.js 18+** (para el dashboard React).
* **Android Studio** (para compilar y ejecutar la app HidroSync).
* Cuenta de **Firebase** con proyecto configurado y archivo `google-services.json` colocado en `app/`.
* Archivo `firebase-credentials.json` (cuenta de servicio) colocado en `proyecto_iot/bridge/`.
* **Clave de API de Cohere** para habilitar HydroBot en la app Android.

## 8. Despliegue y Ejecución

### Opción A — Script automático (recomendado)

Ejecutar desde la raíz del proyecto:

```bat
start-all.bat
```

Levanta en secuencia: Mosquitto (Docker) → Bridge Python → Dashboard React.

### Opción B — Manual paso a paso

**1. Broker Mosquitto**
```bash
cd proyecto_iot
docker compose up -d
```

**2. Bridge MQTT ↔ Firebase**
```bash
cd proyecto_iot/bridge
pip install -r requirements.txt
python bridge.py
```

**3. Dashboard Web**
```bash
cd hidroponia-dashboard
npm install
npm run dev
# Disponible en http://localhost:5173
```

**4. Firmware ESP32**
- Abrir `proyecto_iot/esp32/hidroponia/hidroponia.ino` en Arduino IDE.
- Verificar que `MQTT_BROKER` tenga la IP local del PC (ejecutar `ipconfig` para confirmarla).
- Seleccionar placa **ESP32 Dev Module** y el puerto COM correspondiente.
- Subir con **Ctrl+U** y monitorear en Serial Monitor a 115200 baudios.

**5. App Android**
- instalar y ejecutar en dispositivo físico o emulador.

## 9. Autor

* **Jonathan Uriel Paredes Martínez** — *Ingeniería en Sistemas Computacionales, ESCOM - IPN*
