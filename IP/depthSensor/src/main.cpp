#include <Arduino.h>    // this line is just for PlatformIO, not for ArduinoIDE
// https://github.com/bluerobotics/BlueRobotics_MS5837_Library

#include <Wire.h>
#include "MS5837.h"

MS5837 depthSensor;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(15200);
  Wire.begin();

  depthSensor.setModel(MS5837::MS5837_02BA);

  // density of freshwater kg/m^3
  depthSensor.setFluidDensity(997);
}

void loop() {
  // put your main code here, to run repeatedly:
  depthSensor.read();

  Serial.print("s+");
  Serial.print(depthSensor.depth());
  Serial.println("-e");

  delay(15);
}