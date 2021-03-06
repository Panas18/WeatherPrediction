#include <Adafruit_BMP085.h>

Adafruit_BMP085 bmp;

//Dust Sensor
int measurePin = A0;
int ledPower = 7;

// Uv ray sensor
int UVOUT = A1; //Output from the sensor
int REF_3V3 = A2;

unsigned int samplingTime = 280;
unsigned int deltaTime = 40;
unsigned int sleepTime = 9680;

float voMeasured = 0;
float calcVoltage = 0;
float dustDensity = 0;

void setup()
{
  Serial.begin(9600);
  pinMode(ledPower, OUTPUT);
  while (!bmp.begin())
  {
   Serial.println("Bmp180 sensor not found");
  delay(5000);
  pinMode(UVOUT, INPUT);
  pinMode(REF_3V3, INPUT);2
}


float map_dustDensity(float calVoltage, float in_min, float in_max, float out_min, float out_max)
{
  float m = (out_max - out_min) / (in_max - in_min);
  float output = m * (calVoltage - in_min) + out_min;
  return output;
}

String dust_sensor()
{
  digitalWrite(ledPower, LOW);
  delayMicroseconds(samplingTime);

  voMeasured = analogRead(measurePin);

  delayMicroseconds(deltaTime);
  digitalWrite(ledPower, HIGH);
  delayMicroseconds(sleepTime);
  //Serial.print("calculated Voltage: ");
  //Serial.println(calcVoltage);

  calcVoltage = voMeasured * (5.0 / 1024);
  if (calcVoltage < 3.5)
  {
    dustDensity = map_dustDensity(calcVoltage, 0, 3.5, 0, 500);
  }
  else
  {
    dustDensity = map_dustDensity(calcVoltage, 3.5, 3.72, 500, 800);
  }

  delay(1000);
  return String(dustDensity);
}

String pressure_sensor()
{
  float pressure = bmp.readPressure();
  pressure = pressure / 100;
  return String(pressure)
}

string Uv_sensor(){
  int uvLevel = averageAnalogRead(UVOUT);
  int refLevel = averageAnalogRead(REF_3V3);
  float outputVoltage = 3.3 / refLevel * uvLevel;
  float uvIntensity = mapfloat(outputVoltage, 0.99, 2.8, 0.0, 15.0);
  //Serial.print("output: ");
  //Serial.print(refLevel);

  //Serial.print("ML8511 output: ");
  //Serial.print(uvLevel);

  //Serial.print(" / ML8511 voltage: ");
  //Serial.print(outputVoltage);

  //Serial.print(" / UV Intensity (mW/cm^2): ");
  //Serial.print(uvIntensity);
  delay(100);
  return_string = String(uvIntensity)
 
}

void loop()
{
  String dust_density = dust_sensor();
  String pressure = pressure_sensor();
  String uv_intensity= Uv_sensor();

  String return_message = dust_density + "-" + pressure +"-"+uv_intensity ;
  Serial.println(return_message)
  //Serial.println(return_message);
  //Serial.println(dust_density);
  //Serial.println(uv_intensity);
}

