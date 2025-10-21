#include <Servo.h>
//integer values
int frontleft;
int frontright;
int backleft;
int backright;
int verticalfrontleft;
int verticalfrontright;
int verticalbackleft;
int verticalbackright;
//function/abilities

Servo fl;
Servo fr;
Servo bl;
Servo br;
Servo verfl;
Servo verfr;
Servo verbl;
Servo verbr;

void setup() {
  serial.begin(9600);
  fl.attach(4);
  fr.attach(6);
  bl.attach(10);
  br.attach(8);
  verfl.attach(7);
  verfr.attach(3);
  verbl.attach(5);
  verbr.attach(9);
  delay(2000);
}

void loop() {
  if (Serial.available()){
   frontleft= Serial.readStringUntil('-').toInt();
   Serial.println("FL" + String(frontleft)); 
   fl.writeMicroseconds(frontleft);  
   frontright= Serial.readStringuntil('=').toInt();
   Serial.println(frontright);
   fl.writeMicroseconds("FR"+String(frontright)); 
   backleft = Serial.readStringuntil('+').toInt();
   Serial.println(backleft);
   fl.writeMicroseconds("BL" + String(backleft)); 
   backright = Serial.readStringuntil(',').toInt();
   Serial.println(backright);
   fl.writeMicroseconds("BR" + String(backright)); 
   verticalfrontleft = Serial.readStringuntil(']').toInt();
   Serial.println(verticalfrontleft);
   fl.writeMicroseconds("VFL" + String(verticalfrontleft)); 
   verticalfrontright = Serial.readStringuntil('/').toInt();
   Serial.println(verticalfrontright);
   fl.writeMicroseconds("VFR" + String(verfrontright)); 
  }
}
