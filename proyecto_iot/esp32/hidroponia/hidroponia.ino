/*
 * ============================================================
 *  Hidroponía IoT — ESP32  [MODO PRUEBA — valores simulados]
 *  ESCOM — Sistema de Monitoreo y Control
 * ============================================================
 *
 *  Este sketch NO requiere sensores físicos.
 *  Genera valores aleatorios realistas y los publica por MQTT
 *  para probar el flujo completo:
 *    ESP32 → Mosquitto → bridge.py → Firebase → Dashboard/App
 *
 *  Librería requerida (instalar en Arduino IDE):
 *    - PubSubClient  by Nick O'Leary  (MQTT)
 *
 *  Placa: ESP32 Dev Module
 * ============================================================
 */

#include <WiFi.h>
#include <PubSubClient.h>

// ── WiFi ──────────────────────────────────────────────────────
const char* WIFI_SSID     = "PIXEL";
const char* WIFI_PASSWORD = "123456789";

// ── MQTT Broker (IP local de tu PC) ──────────────────────────
const char* MQTT_BROKER    = "10.150.131.146";    // IP del PC (Wi-Fi hotspot PIXEL)
const int   MQTT_PORT      = 1883;
const char* MQTT_CLIENT_ID = "esp32_hidroponia";

// ── Tópicos ───────────────────────────────────────────────────
const char* TOPIC_TEMP  = "escom/iot/hidroponia/sensores/temperatura";
const char* TOPIC_HUM   = "escom/iot/hidroponia/sensores/humedad";
const char* TOPIC_NIVEL = "escom/iot/hidroponia/sensores/nivel_agua";
const char* TOPIC_BOMBA = "escom/iot/hidroponia/actuadores/bomba";

// ── Pin bomba (relé) ──────────────────────────────────────────
#define BOMBA_PIN  2    // LED integrado ESP32 (GPIO 2) — activo en HIGH

// ── Intervalo de publicación ──────────────────────────────────
const unsigned long INTERVALO_MS = 5000;  // cada 5 segundos

// ── Valores simulados (varían suavemente entre ciclos) ────────
float simTemp  = 22.0;   // °C   rango normal: 18–26
float simHum   = 60.0;   // %    rango normal: 50–70
float simNivel = 18.0;   // cm   rango normal: 10–30

// ── Objetos ───────────────────────────────────────────────────
WiFiClient   wifiClient;
PubSubClient mqtt(wifiClient);

unsigned long ultimaPublicacion = 0;

// =============================================================
//  WiFi
// =============================================================
void conectarWiFi() {
  Serial.print("\nConectando a WiFi");
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi OK — IP: " + WiFi.localIP().toString());
}

// =============================================================
//  MQTT — callback (mensajes entrantes)
// =============================================================
void onMensaje(char* topic, byte* payload, unsigned int len) {
  String msg = "";
  for (unsigned int i = 0; i < len; i++) msg += (char)payload[i];

  Serial.println("MQTT entrada [" + String(topic) + "] => " + msg);

  if (String(topic) == TOPIC_BOMBA) {
    if (msg == "ON") {
      digitalWrite(BOMBA_PIN, HIGH);   // LED ON
      Serial.println(">>> Bomba ENCENDIDA (LED ON)");
    } else if (msg == "OFF") {
      digitalWrite(BOMBA_PIN, LOW);    // LED OFF
      Serial.println(">>> Bomba APAGADA  (LED OFF)");
    }
  }
}

// =============================================================
//  MQTT — conexión con reintentos
// =============================================================
void conectarMQTT() {
  while (!mqtt.connected()) {
    Serial.print("Conectando a MQTT...");
    if (mqtt.connect(MQTT_CLIENT_ID)) {
      Serial.println(" OK");
      // Suscribirse al tópico de la bomba (QoS 1 — máximo de PubSubClient)
      mqtt.subscribe(TOPIC_BOMBA, 1);
      Serial.println("Suscrito: " + String(TOPIC_BOMBA));
    } else {
      Serial.println(" fallo rc=" + String(mqtt.state()) + " | reintento en 3s");
      delay(3000);
    }
  }
}

// =============================================================
//  Simulación — genera variaciones pequeñas y realistas
// =============================================================
float variar(float valor, float delta, float minVal, float maxVal) {
  // Suma un delta aleatorio pequeño y mantiene el valor en rango
  float cambio = ((float)random(-100, 100) / 100.0) * delta;
  valor += cambio;
  if (valor < minVal) valor = minVal;
  if (valor > maxVal) valor = maxVal;
  return valor;
}

// =============================================================
//  Setup
// =============================================================
void setup() {
  Serial.begin(115200);
  randomSeed(analogRead(0));  // semilla aleatoria con pin flotante

  pinMode(BOMBA_PIN, OUTPUT);
  digitalWrite(BOMBA_PIN, LOW);   // LED apagado por defecto (bomba OFF)

  conectarWiFi();

  mqtt.setServer(MQTT_BROKER, MQTT_PORT);
  mqtt.setCallback(onMensaje);
  mqtt.setKeepAlive(60);
}

// =============================================================
//  Loop
// =============================================================
void loop() {
  // Mantener conexión MQTT
  if (!mqtt.connected()) conectarMQTT();
  mqtt.loop();

  unsigned long ahora = millis();
  if (ahora - ultimaPublicacion < INTERVALO_MS) return;
  ultimaPublicacion = ahora;

  char buf[10];

  // ── Actualizar valores simulados ──────────────────────────
  simTemp  = variar(simTemp,  0.5, 16.0, 30.0);
  simHum   = variar(simHum,   1.0, 45.0, 75.0);
  simNivel = variar(simNivel, 0.8,  8.0, 32.0);

  // ── Publicar temperatura (QoS 0) ─────────────────────────
  dtostrf(simTemp, 5, 1, buf);
  mqtt.publish(TOPIC_TEMP, buf);
  Serial.println("[SIM] Temperatura : " + String(buf) + " °C");

  // ── Publicar humedad (QoS 0) ──────────────────────────────
  dtostrf(simHum, 5, 1, buf);
  mqtt.publish(TOPIC_HUM, buf);
  Serial.println("[SIM] Humedad     : " + String(buf) + " %");

  // ── Publicar nivel de agua (QoS 0) ────────────────────────
  dtostrf(simNivel, 5, 1, buf);
  mqtt.publish(TOPIC_NIVEL, buf);
  Serial.println("[SIM] Nivel agua  : " + String(buf) + " cm");

  Serial.println("────────────────────────");
}
