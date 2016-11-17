#include <ESP8266WiFi.h>
#include <WiFiClient.h>

// WiFi information
const char* WIFI_SSID = "Lampu";
const char* WIFI_PSK = "babyzita";

// Remote site information
const char* website = "192.168.1.110";
const int port = 15151;
const char* siteOn = "192.168.1.110/LED=ON";
const char* siteOff = "192.168.1.110/LED=OFF";

// variable states that will change
int lightState = 0;
int lastlightState = 0;

// Pin definitions
const int LED_PIN = 5;
const int switchOn = 7;
// const int switchOff = 2;
// const int relay = 7;

// Global variables
WiFiClient client;

void setup() {

  // Set up serial console to read web page
  Serial.begin(115200);
  Serial.print("Front Light Switch");

  // Set up LED for debugging
  pinMode(LED_PIN, OUTPUT);

  // Set up switch pinMode
  pinMode(switchOn, INPUT_PULLUP);
  //pinMode(switchOff, INPUT_PULLUP);

  // Setting lights on by default

  digitalWrite(switchOn, HIGH);
  lightState = digitalRead(switchOn);

  // Connect to WiFi
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PSK);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");



  // Attempt to connect to website
  if ( !getPage() ) {
    Serial.println("GET request failed");
  }
}

void loop() {

int lightState = digitalRead(switchOn);

  // If there are incoming bytes, print them
  if ( client.available() ) {
    char c = client.read();
    Serial.print(c);
  }

  // If the server has disconnected, stop the client and WiFi
  if ( !client.connected() ) {
    Serial.println();

    // Close socket and wait for disconnect from WiFi
    client.stop();
    if ( WiFi.status() != WL_DISCONNECTED ) {
      WiFi.disconnect();
    }

    // Turn off LEDss
    digitalWrite(LED_PIN, LOW);

    // Do nothing
    Serial.println("Finished Thing GET test");
    while(true){
      delay(1000);
    }
  }
}

// Attempt to connect to WiFi
void connectWiFi() {

  byte led_status = 0;

  // Set WiFi mode to station (client)
//  WiFi.mode(WIFI_STA);

  // Initiate connection with SSID and PSK
  WiFi.begin(WIFI_SSID, WIFI_PSK);

  // Blink LED while we wait for WiFi connection
  while ( WiFi.status() != WL_CONNECTED ) {
    digitalWrite(LED_PIN, led_status);
    led_status ^= 0x01;
    delay(100);
  }

  // Turn LED on when we are connected
  digitalWrite(LED_PIN, HIGH);
}

// Perform an HTTP GET request to a remote page
bool getPage() {

  // Attempt to make a connection to the remote server

if (digitalRead(switchOn) == HIGH  && lightState == LOW)  {
    client.connect(siteOn, port);
    Serial.println("Lights on");
}
if  (digitalRead(switchOn) == LOW && lightState == HIGH) {
    client.connect(siteOff, port);
    Serial.println("Lights off");
}
  if ( !client.connect(website, port) ) {
    return false;
  }

  // Make an HTTP GET request
  client.println("GET /index.html HTTP/1.1");
  client.print("Host: ");
  client.println(website);
  client.println("Connection: close");
  client.println();

  return true;
}
