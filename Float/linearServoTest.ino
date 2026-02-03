#include <Servo.h>

Servo linearServo;

void setup() {
  linearServo.attach(9);    // MEGA pin 9
}

void loop() {
  // Extend
  linearServo.writeMicroseconds(2000);  
  delay(2000);

  // Half way
  linearServo.writeMicroseconds(1500);  
  delay(2000);

  // Retract
  linearServo.writeMicroseconds(1000);  
  delay(2000);
}
