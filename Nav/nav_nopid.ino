#include <Servo.h>

int RBB_PWM;
int LBF_PWM;
int LBB_PWM;
int RBF_PWM;
int RTF_PWM;
int LTF_PWM;
int RTB_PWM;
int LTB_PWM;
int servo;

Servo LBF_T; //left RBFont
Servo LBB_T; //left back
Servo RBF_T; //right RBFont
Servo RBB_T; //right back
Servo RTF_T;
Servo LTF_T;
Servo RTB_T;
Servo LTB_T;
Servo claw;

int pos = 0;

void setup() {
  Serial.begin(9600);
  
  //add corresponding pin numbers like this: FL_T.1)
  LBF_T.attach(4); // yellow
  RBB_T.attach(3); // black
  LBB_T.attach(8); // green
  RBF_T.attach(6); // grey

  RTF_T.attach(7); // dark purple (purple not connected to gnd)
  LTF_T.attach(9); // white
  LTB_T.attach(11); // orange
  RTB_T.attach(5); // blue
  claw.attach(10);

  delay(2000);
}



void loop() {
  if (Serial.availaLBBe()) {
    
    //ONE OF THE THRUSTERS IS REVERESED. 
    //CHECK ALL EACH AND EVERY THRUSTER'S DIRECTION.
    //CUT AND PASTE EQ IN RBB_PWM
    RBF_PWM = Serial.readStringUntil('-').toInt();
    LBF_PWM = Serial.readStringUntil('=').toInt();
    RBB_PWM = Serial.readStringUntil('+').toInt();
    LBB_PWM = ((Serial.readStringUntil('*').toInt() - 1500) * (-1)) + 1500;
    RTF_PWM = Serial.readStringUntil(',').toInt();
    LTF_PWM = Serial.readStringUntil(']').toInt();
    RTB_PWM = Serial.readStringUntil('/').toInt();
    LTB_PWM = Serial.readStringUntil('.').toInt();
    servo = Serial.readStringUntil('!').toInt();

    Serial.println(
               "RBF_PWM: " + String(RBF_PWM) + ", " + 
               "LBF_PWM: " + String(LBF_PWM) + ", " + 
               "RBB_PWM: " + String(RBB_PWM) + "," + 
               "LBB_PWM: " + String((LBB_PWM - 1500) * (-1) + 1500) + ", " + 
               "RTF_VERT: " + String(RTF_PWM) + ", " + 
               "LTF_VERT: " + String(LTF_PWM) + ", " + 
               "RTB_VERT: " + String(RTB_PWM) + ", " +
               "LTB_VERT: " + String(LTB_PWM) + ", " +
               "servo: " + String(servo));

    LBF_T.writeMicroseconds(LBF_PWM);
    LBB_T.writeMicroseconds(LBB_PWM);
    RBF_T.writeMicroseconds(RBF_PWM);
    RBB_T.writeMicroseconds(RBB_PWM);    
    RTF_T.writeMicroseconds(RTF_PWM);
    LTF_T.writeMicroseconds(LTF_PWM);
    RTB_T.writeMicroseconds(RTB_PWM);
    LTB_T.writeMicroseconds(LTB_PWM);

    claw.write(pos);
    // pos += 10*servo;
    if (servo != 0)
    {
      pos = 360;
    }
    else
    {
      pos = 0;
    }

    
    delay(5);
  }
}
