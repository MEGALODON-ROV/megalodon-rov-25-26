#include <Servo.h>

// thruster variables
int frontLeft;
int frontRight;
int backLeft;
int backRight;
int vertical;

// change variables into Servo objects
Servo frontLeft;
Servo frontRight;
Servo backLeft;
Servo backRight;
Servo vertical;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);   // set frequency = able to print

  // set all thrusters to their pin numbers
  frontLeft.attach(3);
  frontRight.attach(5);
  backLeft.attach(6);
  backRight.attach(9);
  vertical.attach(10);
}
/*
// from my Python code for creating the message to send to Arduino
parts = [
        str(thrusters["frontLeft"]),  "+",
        str(thrusters["frontRight"]), "-",
        str(thrusters["backLeft"]),   "=",
        str(thrusters["backRight"]),  "/",
        str(thrusters["vertical"]),   ")",      # there are 4 vertical thrusters
        str(thrusters["vertical"]),   "(",      # but they are all have the same output
        str(thrusters["vertical"]),   "!",
        str(thrusters["vertical"])
    ]
*/
void loop() {
  if (Serial.available()) {
    // read the message of pwm values
    int FLValue = Serial.readStringUntil('+').toInt();
    Serial.println("FL: " + String(FLValue));
    frontLeft.writeMicroseconds(FLValue);

    int FRValue = Serial.readStringUntil('-').toInt();
    Serial.println("FR: " + String(FRValue));
    frontRight.writeMicroseconds(FRValue);

    int BLValue = Serial.readStringUntil('=').toInt();
    Serial.println("BL: " + String(BLValue));
    backLeft.writeMicroseconds(BLValue);

    int BRValue = Serial.readStringUntil('/').toInt();
    Serial.println("BR: " + String(BRValue));
    backRight.writeMicroseconds(BRValue);

    int vertical = Serial.readStringUntil(')').toInt();
    Serial.println("Vertical: " + String(vertical));
    vertical.writeMicroseconds(vertical);
  }
}
