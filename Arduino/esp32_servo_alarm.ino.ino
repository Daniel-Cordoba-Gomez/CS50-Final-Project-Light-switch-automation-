#include <WiFi.h>
#include <WebServer.h>
#include <ESP32Servo.h>
#include <time.h>

const char* SSID = "FABULAB";           
const char* PASSWORD = "ROUTERCASA01";  

WebServer server(80);
Servo myServo;
String status = "rest";

// Alarm variables
int alarmHour = -1;
int alarmMinute = -1;
bool alarmSet = false;
bool alarmTriggered = false;
unsigned long alarmStartMillis = 0;
const unsigned long ALARM_DURATION = 10 * 60 * 1000UL; // 10 minutes

// ---------------- Setup Routes ---------------- //

void handleControl() {
  if (!server.hasArg("action")) {
    server.send(400, "application/json", "{\"error\":\"Missing action\"}");
    return;
  }

  String action = server.arg("action");

  if (action == "on" && status == "rest") {
    myServo.write(90);
    status = "pressed";
    Serial.println("[CONTROL] Switch ON");
    server.send(200, "application/json", "{\"message\": \"Light turned on\"}");
  } else if (action == "off" && status == "pressed") {
    myServo.write(0);
    status = "rest";
    Serial.println("[CONTROL] Switch OFF");
    server.send(200, "application/json", "{\"message\": \"Light turned off\"}");
  } else {
    server.send(400, "application/json", "{\"error\": \"Invalid state transition\"}");
  }
}

void handleAlarm() {
  if (!server.hasArg("hour") || !server.hasArg("minute")) {
    server.send(400, "application/json", "{\"error\":\"Missing hour or minute\"}");
    return;
  }

  alarmHour = server.arg("hour").toInt();
  alarmMinute = server.arg("minute").toInt();
  alarmSet = true;
  alarmTriggered = false;

  Serial.printf("[ALARM] Set for %02d:%02d\n", alarmHour, alarmMinute);
  server.send(200, "application/json", "{\"message\": \"Alarm scheduled\"}");
}

// ---------------- Setup & Loop ---------------- //

void setup() {
  Serial.begin(115200);

  // Connect to Wi-Fi
  WiFi.begin(SSID, PASSWORD);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected to WiFi.");
  Serial.print("ESP32 IP: ");
  Serial.println(WiFi.localIP());

  // Attach servo
  myServo.attach(13);  // ✅ Update pin if needed
  myServo.write(0);

  // Setup routes
  server.on("/control", HTTP_POST, handleControl);
  server.on("/alarm", HTTP_POST, handleAlarm);
  server.begin();
  Serial.println("HTTP server started");

  // NTP Time Sync
  configTime(0, 0, "pool.ntp.org", "time.nist.gov");
  Serial.print("Syncing NTP time");
  struct tm timeinfo;
  while (!getLocalTime(&timeinfo)) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nTime synchronized.");
}

void loop() {
  server.handleClient();

  if (alarmSet && !alarmTriggered) {
    struct tm timeinfo;
    if (getLocalTime(&timeinfo)) {
      if (timeinfo.tm_hour == alarmHour && timeinfo.tm_min == alarmMinute) {
        Serial.println("[ALARM] Triggered. Turning ON switch.");
        myServo.write(90);
        status = "pressed";
        alarmTriggered = true;
        alarmStartMillis = millis();
      }
    }
  }

  // Turn off after 10 minutes
  if (alarmTriggered && millis() - alarmStartMillis >= ALARM_DURATION) {
    Serial.println("[ALARM] Auto OFF after 10 minutes.");
    myServo.write(0);
    status = "rest";
    alarmSet = false;
    alarmTriggered = false;
  }
}
