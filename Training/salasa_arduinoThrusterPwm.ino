
#include <Servo.h>

//declare thruster values the PWM, not the thruster
int fl_PWM;
int fr_PWM;
int br_PWM;
int bl_PWM;
int vertical1_PWM;

//create servo objects . the literal thruster
Servo fl;
Servo fr;
Servo br;
Servo bl;
Servo vertical1;

//attach thrusters(servo) to pins 
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  fl.attach(11);
  fr.attach(10);
  br.attach(9);
  bl.attach(6);
  vertical1.attach(5);
  delay(2000);
}

void loop() {
  // put your main code here, to run repeatedly:
  // read values from Serial
if (Serial.available()) {
  fl_PWM = Serial.readStringUntil(',').toInt();
  fr_PWM = Serial.readStringUntil('/').toInt();
  br_PWM = Serial.readStringUntil(':').toInt();
  bl_PWM = Serial.readStringUntil('#').toInt();
  vertical1 = Serial.readStringUntil('*').toInt();
//print values
  Serial.println("FL_PWM: " + String(fl_PWM));
  Serial.println("FR_PWM: " + String(fr_PWM));
  Serial.println("BR_PWM: " + String(br_PWM));
  Serial.println("BL_PWM: " + String(bl_PWM));
  Serial.println("VERTICAL1_PWM: " + String(vertical1_PWM));
//send values to thrusters
  fl.writeMicroseconds(fl_PWM);
  fr.writeMicroseconds(fr_PWM);
  br.writeMicroseconds(bl_PWM);
  bl.writeMicroseconds(br_PWM);
  vertical1.writeMicroseconds(vertical1_PWM);



}
}



}
