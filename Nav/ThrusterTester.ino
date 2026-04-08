
#include <Servo.h>

int BR_PWM;
int FL_PWM;
int BL_PWM;
int FR_PWM;
int VTR_PWM;
int VTL_PWM;
int VBR_PWM;
int VBL_PWM;

Servo FL_T; //left front
Servo BL_T; //left back
Servo FR_T; //right front
Servo BR_T; //right back
Servo VTR_T;
Servo VTL_T;
Servo VBR_T;
Servo VBL_T;

Servo[] Thrusters = {FL_T, BL_T, FR_T, BR_T, VTR_T, VTL_T, VBR_T, VBL_T};

boolean test = true;


void setup() {
  Serial.begin(9600);

  //add corresponding pin numbers like this: FL_T.attach(1)
  FL_T.attach(4); //
  BR_T.attach(11); //
  BL_T.attach(8); //
  FR_T.attach(6); //

  VTR_T.attach(7);
  VTL_T.attach(9);
  VBR_T.attach(5); //
  VBL_T.attach(3); // 3.1 back, 2.8 forward

  FL_T.writeMicroseconds(1500);
  BL_T.writeMicroseconds(1500);
  FR_T.writeMicroseconds(1500);
  BR_T.writeMicroseconds(1500);    
  VTR_T.writeMicroseconds(1500);
  VTL_T.writeMicroseconds(1500);
  VBR_T.writeMicroseconds(1500);
  VBL_T.writeMicroseconds(1500);

  delay(2000);
}



void loop()
{
  if (test)
  {
    for (int i = 0; i < Thrusters.length; i++)
    {
      Servo thruster = Thrusters[i];
      thruster.writeMicroseconds(1600);
      delay(1500);
      thruster.writeMicroseconds(1500);
      delay(1500)
    }
    test = false;
  }
  
}
