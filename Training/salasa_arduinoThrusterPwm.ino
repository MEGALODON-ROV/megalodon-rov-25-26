
#include <Servo.h>

//declare thruster values
int FR_value;
int FL_value;
int BR_value;
int BL_value;
int V_value;

//servo objects
Servo FR_value;
Servo FL_value;
Servo BR_value;
Servo BL_value;
Servo V_value;

//attach thrusters to pins (PWM)
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  FR_value.attach(11);
  FL_value.attach(10);
  BR_value.attach(9);
  BL_value.attach(6);
  V_value.attach(5);
}

void loop() {
  // put your main code here, to run repeatedly:
  // read values from Serial
if (Serial.available()) {
  int fl = Serial.readStringUntil(',').toInt();
  int fr = Serial.readStringUntil('/').toInt();
  int bl = Serial.readStringUntil(':').toInt();
  int br = Serial.readStringUntil('#').toInt();
  int vertical1 = Serial.readStringUntil('*').toInt();

  Serial.println(fl);
  Serial.println(fr);
  Serial.println(bl);
  Serial.println(br);
  Serial.println(vertical1);

  FR_value.WriteMicroseconds(fl);
  FL_value.WriteMicroseconds(fr);
  BR_value.WriteMicroseconds(bl);
  BL_value.WriteMicroseconds(br);
  V_value.WriteMicroseconds(vertical1);



}
}



}
