#include <Arduino.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>
#include "accelerometerTesting.h"

Adafruit_MPU6050 mpu;

void initializeMPU() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.println("Initializing MPU6050");

  while(!mpu.begin()) {
    Serial.println("can't find mpu");
    delay(500);
  }

  Serial.println("found mpu");
}

void readMPU() {
  // put your main code here, to run repeatedly:
  Serial.println("entered loop");
  sensors_event_t a, g, temp;     // acceleration, gyroscope, temperature
  mpu.getEvent(&a, &g, &temp);

  //Serial.print("X raw: ");
  Serial.println(a.acceleration.x);
  //Serial.print("Y raw: ");
  Serial.println(a.acceleration.y);
  //Serial.print("Z raw: ");
  Serial.println(a.acceleration.z);
  delay(10);
}