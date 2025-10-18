
#include <Servo.h>

//declare thruster values
int fl;
int fr;
int br;
int bl;
int vertical1;

//create servo objects
Servo fl;
Servo fr;
Servo br;
Servo bl;
Servo vertical1;

//attach thrusters to pins (PWM)
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  fl.attach(11);
  fr.attach(10);
  br.attach(9);
  bl.attach(6);
  vertical1.attach(5);
}

void loop() {
  // put your main code here, to run repeatedly:
  // read values from Serial
if (Serial.available()) {
  int fl_value = Serial.readStringUntil(',').toInt();
  int fr_value = Serial.readStringUntil('/').toInt();
  int br_value = Serial.readStringUntil(':').toInt();
  int bl_value = Serial.readStringUntil('#').toInt();
  int vertical1_value = Serial.readStringUntil('*').toInt();
//print values
  Serial.println("FL_PWM: " + String(fl_value));
  Serial.println("FR_PWM: " + String(fr_value));
  Serial.println("BR_PWM: " + String(br_value));
  Serial.println("BL_PWM: " + String(bl_value));
  Serial.println("VERTICAL1_PWM: " + String(vertical1_value));
//send values to thrusters
  fl.writeMicroseconds(fl_value);
  fr.writeMicroseconds(fr_value);
  br.writeMicroseconds(bl_value);
  bl.writeMicroseconds(br_value);
  vertical1.writeMicroseconds(vertical1_value);



}
}



}
