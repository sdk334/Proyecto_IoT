# Sistema de Monitoreo y Control IoT para Hidroponía 
## 1. Descripción del Proyecto
Este proyecto implementa una arquitectura IoT para el monitoreo y control automatizado de un sistema hidropónico. Combina la eficiencia y ligereza del protocolo MQTT en la capa Edge con la sincronización en tiempo real de Firebase en la capa Cloud. Permite la lectura de sensores y el accionamiento de bombas de agua tanto desde una interfaz web como desde una aplicación móvil. Además, incorpora un **chat de IA** que asiste al usuario resolviendo dudas sobre el funcionamiento del sistema y el cuidado del cultivo hidropónico.
![torre de hidroponia](/imagenes/torre_hidroponia.jpg)
## 2. Arquitectura del Sistema
La arquitectura se divide en tres capas interconectadas:
* **Capa Edge (Hardware y MQTT):** Microcontroladores (ESP32) que publican datos de sensores y escuchan comandos de actuadores a través de un Broker Eclipse Mosquitto.
* **Capa Cloud e Integración (Firebase):** Un servicio puente (Bridge) que conecta el tráfico MQTT con Firebase Realtime Database/Firestore para almacenamiento y sincronización en tiempo real.
* **Capa de Aplicación (Frontend):**
    * **Dashboard Web:** Interfaz desarrollada con React.
    * **Aplicación Móvil:** App nativa para Android para monitoreo portátil y control remoto.
    * **Chat de IA:** Asistente conversacional integrado en la interfaz que responde dudas del usuario sobre el sistema, la interpretación de las lecturas de sensores y recomendaciones para el cultivo.
## 3. Tecnologías Propuestas
* **Microcontrolador:** ESP32 devkit
* **Lenguaje de Firmware:** C/C++ (Framework Arduino)
* **Broker MQTT:** Mosquitto
* **Backend / Base de Datos:** Firebase 
* **Servicio Puente (Bridge):** Python
* **Frontend Web:** React
* **Aplicación Móvil:** Android
* **Chat de IA:** Integración con API de modelo de lenguaje para la asistencia al usuario
* **Despliegue de Broker:** Docker y Docker Compose
## 4. Árbol de Tópicos MQTT
El sistema utiliza una estructura jerárquica, empleando niveles de Calidad de Servicio
| Tópico | num | Descripción | Dirección |
| :--- | :---: | :--- | :---: |
| `escom/iot/hidroponia/sensores/temperatura` | 0 | Lectura de temperatura ambiente | ESP32 -> Broker |
| `escom/iot/hidroponia/sensores/nivel_agua` | 1 | Nivel del tanque de solución | ESP32 -> Broker |
| `escom/iot/hidroponia/actuadores/bomba` | 2 | Comando para encendido/apagado | Firebase -> Bridge -> Broker -> ESP32 |
## 5. Chat de IA para Asistencia al Usuario
El sistema integra un asistente conversacional basado en IA que permite al usuario resolver dudas de forma interactiva. Sus funciones principales son:
* **Resolución de dudas:** Responde preguntas sobre el funcionamiento del sistema, la configuración y el uso de la interfaz.
* **Interpretación de datos:** Ayuda al usuario a comprender las lecturas de los sensores (temperatura, nivel de agua) y su impacto en el cultivo.
* **Recomendaciones:** Ofrece sugerencias sobre el cuidado del sistema hidropónico y posibles acciones ante valores anómalos.

El chat se encuentra accesible directamente desde el Dashboard Web y la aplicación móvil.
## 6. Requisitos Previos
* Docker y Docker Compose (para el contenedor de Mosquitto).
* Python instalado para ejecutar el servicio puente.
* Una cuenta activa de Google/Firebase con un proyecto configurado.
* Entorno de desarrollo C/C++ para compilar el firmware del ESP32.
* Clave de API válida del proveedor del modelo de IA para habilitar el chat.
## 7. Despliegue y Ejecución
1.  **Levantar el Broker:** Ejecutar `docker-compose up -d` en el directorio raíz para iniciar Mosquitto.
2.  **Iniciar el Puente MQTT-Firebase:** Instalar dependencias con `npm install` y ejecutar `node bridge.js`.
3.  **Frontend:** Instalar dependencias con `npm install`, ejecutar `npm start` para desarrollo o `npm run build` para generar la versión de producción y desplegarla con Firebase Hosting.
## 8. Autor
* **Jonathan Uriel Paredes Martínez** - *Ingeniería en Sistemas Computacionales, ESCOM - IPN*
