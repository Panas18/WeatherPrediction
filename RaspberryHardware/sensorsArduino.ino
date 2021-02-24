#include <Adafruit_BMP085.h>

Adafruit_BMP085 bmp;
int measurePin = A0;
int ledPower = 7;

unsigned int samplingTime = 280;
unsigned int deltaTime = 40;
unsigned int sleepTime = 9680;

float voMeasured = 0;
float calcVoltage = 0;
float dustDensity = 0;

void setup() {
  Serial.begin(9600);
  pinMode(ledPower, OUTPUT);
  while (!bmp.begin()) {
    Serial.println("Bmp180 sensor not found");
    delay(5000);
  }
}


float map_dustDensity(float calVoltage , float in_min, float in_max, float out_min, float out_max)
{
  float m = (out_max - out_min) / (in_max - in_min);
  float output = m * (calVoltage - in_min) + out_min;
  return output;
}

String dust_sensor() {
  digitalWrite(ledPower, LOW);
  delayMicroseconds(samplingTime);

  voMeasured = analogRead(measurePin);

  delayMicroseconds(deltaTime);
  digitalWrite(ledPower, HIGH);
  delayMicroseconds(sleepTime);

  calcVoltage = voMeasured * (5.0 / 1024);
  if (calcVoltage < 3.5) {
    dustDensity = map_dustDensity(calcVoltage, 0, 3.5, 0, 500);
  } else {
    dustDensity = map_dustDensity(calcVoltage, 3.5 , 3.72, 500, 800);
  }

  delay(1000);
  return String(dustDensity);


}

String pressure_sensor() {
  float  pressure = bmp.readPressure();
  pressure = pressure / 100;
  return String(pressure);
}

void loop() {
  String  dust_density = dust_sensor();
  String pressure = pressure_sensor();

  String return_message = dust_density + "-" + pressure;
  Serial.println(return_message);

}
