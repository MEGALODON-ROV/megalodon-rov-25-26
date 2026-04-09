
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



boolean test = true;


void setup() {
  Serial.begin(9600);

  //add corresponding pin numbers like this: FL_T.attach(1)
  LBF_T.attach(4); // yellow
  RBB_T.attach(11); // black
  LBB_T.attach(8); // green
  RBF_T.attach(6); // grey

  RTF_T.attach(7); // dark purple (purple not connected to gnd)
  LTF_T.attach(9); // white
  LTB_T.attach(5); // orange
  RTB_T.attach(3); // blue

  FL_T.writeMicroseconds(1500); //
  BR_T.writeMicroseconds(1500); //
  BL_T.writeMicroseconds(1500); //
  FR_T.writeMicroseconds(1500); //

  VTR_T.writeMicroseconds(1500);
  VTL_T.writeMicroseconds(1500);
  VBR_T.writeMicroseconds(1500); //
  VBL_T.writeMicroseconds(1500);

  
  delay(5000);
}



void loop()
{
    
  
  // if test
  // {
    // Servo Thrusters[8] = {FL_T, BL_T, FR_T, BR_T, VTR_T, VTL_T, VBR_T, VBL_T};

  VBL_T.writeMicroseconds(1600);
  delay(2500);
  VBL_T.writeMicroseconds(1500);
  delay(500);
  VBR_T.writeMicroseconds(1600);
  delay(2500);
  VBR_T.writeMicroseconds(1500);
  delay(500);
  BR_T.writeMicroseconds(1600);
  delay(2500); //
  BR_T.writeMicroseconds(1600);
  delay(500);
    

  //   for (int i = 0; i < 8; i++)
  //   {
  //     Thrusters[i].writeMicroseconds(1500);
  //   }
    
  //   for (int i = 0; i < 8; i++)
  //   {
  //     Servo thruster = Thrusters[i];
  //     thruster.writeMicroseconds(1600);
  //     delay(2500);
  //     thruster.writeMicroseconds(1500);
  //     delay(500);
  //   }

  //   test = false;

  //   delay(1500);
  // }
  // // FL_T.writeMicroseconds(1600); //
  // BR_T.writeMicroseconds(1600); //
  // BL_T.writeMicroseconds(1600); //
  // FR_T.writeMicroseconds(1600); //

  // VTR_T.writeMicroseconds(1600);
  // VTL_T.writeMicroseconds(1600);
  // VBR_T.writeMicroseconds(1600); //
  // VBL_T.writeMicroseconds(1600);

  // delay(5000);

  // FL_T.writeMicroseconds(1500); //
  // BR_T.writeMicroseconds(1500); //
  // BL_T.writeMicroseconds(1500); //
  // FR_T.writeMicroseconds(1500); //

  // VTR_T.writeMicroseconds(1500);
  // VTL_T.writeMicroseconds(1500);
  // VBR_T.writeMicroseconds(1500); //
  // VBL_T.writeMicroseconds(1500);
  
}
