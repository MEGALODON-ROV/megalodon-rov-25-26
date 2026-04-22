#include <ESP32Servo.h>

Servo linearServo;

void setup() {
  linearServo.attach(17);    // MEGA pin 9
}

void loop() {
  // Extend
  linearServo.writeMicroseconds(2300);  
  delay(2000);

  // Retract
  linearServo.writeMicroseconds(600);  
  delay(2000);
}
