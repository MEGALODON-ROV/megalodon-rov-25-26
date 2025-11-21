#include <MPU6050.h>
#include <Wire.h>

MPU6050 mpu;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  Serial.println("Initializing MPU6050");

  Serial.println("ANGRYYYYYYY");
  while(!mpu.begin(MPU6050_SCALE_2000DPS, MPU6050_RANGE_2G)) {
    Serial.println("can't find mpu");
    delay(500);
  }

  Serial.println("found mpu");
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.println("entered loop");
  Vector rawAccel = mpu.readRawAccel();
  Vector normAccel = mpu.readNormalizeAccel();

  Serial.print("X raw: ");
  Serial.println(rawAccel.XAxis);
  Serial.print("Y raw: ");
  Serial.println(rawAccel.YAxis);
  Serial.print("Z raw: ");
  Serial.println(rawAccel.ZAxis);

  Serial.print("X norm: ");
  Serial.println(normAccel.XAxis);
  Serial.print("Y norm: ");
  Serial.println(normAccel.YAxis);
  Serial.print("Z norm: ");
  Serial.println(normAccel.ZAxis);

  delay(10);
}