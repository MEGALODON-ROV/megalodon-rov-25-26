#include <ESP32Servo.h>

Servo linearServo;

const int servoPin = 17;     // change if needed
const int servoMin = 600;    // adjust to your servo
const int servoMax = 2300;   // adjust to your servo

void setup() {
  Serial.begin(115200);
  delay(1000);

  linearServo.attach(servoPin);

  Serial.println("Servo test starting...");
}

void loop() {

  // extend (min → max)
  for (int pulse = servoMin; pulse <= servoMax; pulse += 20) {
    linearServo.writeMicroseconds(pulse);
    Serial.println(pulse);
    delay(30);
  }

  delay(1000);

  // retract (max → min)
  for (int pulse = servoMax; pulse >= servoMin; pulse -= 20) {
    linearServo.writeMicroseconds(pulse);
    Serial.println(pulse);
    delay(30);
  }

  delay(1000);
}
