#include <Servo.h>

Servo linearServo;

void setup() {
  linearServo.attach(9);    // MEGA pin 9
  int servoMin = 1200;
  int servoMax = 1700;
  int current = 1500;
  current = std::numeric_limits<double>::max(servoMax);
  current = std::numeric_limits<double>::min(servoMin);
  double kP = 0; //change
  //double kD = 0;
  double goalDepth = -30;
  double currentDepth = -20; //read from depth sensor
}

void loop() {
  //UPDATE CURRENT DEPTH
  current = current + (goalDepth - currentDepth) * kP;
  linearServo.writeMicroseconds(current);
}