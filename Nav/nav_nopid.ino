#include <Servo.h>
#include "MS5837.h"

MS5837 depthSensor;

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
  LBF_T.attach(3); // yellow
  RBB_T.attach(5); // black
  LBB_T.attach(8); // green
  RBF_T.attach(6); // grey

  RTF_T.attach(7); // dark purple (purple not connected to gnd)
  LTF_T.attach(9); // white
  LTB_T.attach(2); // orange
  RTB_T.attach(11); // blue

  claw.attach(4);

  initDepthSensor(7);

  delay(2000);
}

void initDepthSensor(int channel) {
  delay(500);

  Serial.println("Intializing Depth Sensor...");
  // selectChannel(channel);

  while (!depthSensor.init()) {
    Serial.println("Init failed!");
    Serial.println("Are SDA/SCL connected correctly?");
    Serial.println("Blue Robotics Bar30: White=SDA, Green=SCL");
    Serial.println("\n\n\n");
    delay(5000);
  }

  depthSensor.setModel(MS5837::MS5837_02BA);
  depthSensor.setFluidDensity(997);
  depthSensor.init();

  Serial.println("Success!\n");

  delay(500);
}

void loop() {
  if (Serial.available()) {
    
    //ONE OF THE THRUSTERS IS REVERESED. 
    //CHECK ALL EACH AND EVERY THRUSTER'S DIRECTION.
    //CUT AND PASTE EQ IN RBB_PWM
    RBF_PWM = Serial.readStringUntil('-').toInt();
    LBF_PWM = Serial.readStringUntil('=').toInt();
    RBB_PWM = Serial.readStringUntil('+').toInt();
    LBB_PWM = Serial.readStringUntil('*').toInt();
    RTF_PWM = Serial.readStringUntil(',').toInt();
    LTF_PWM = Serial.readStringUntil(']').toInt();
    RTB_PWM = Serial.readStringUntil('/').toInt();
    LTB_PWM = Serial.readStringUntil('.').toInt();
    servo = Serial.readStringUntil('!').toInt();

    // depthSensor.read();

    Serial.println(
               "RBF_PWM: " + String(RBF_PWM) + ", " + 
               "LBF_PWM: " + String(LBF_PWM) + ", " + 
               "RBB_PWM: " + String(RBB_PWM) + "," + 
               "LBB_PWM: " + String(LBB_PWM) + ", " + 
               "RTF_VERT: " + String(RTF_PWM) + ", " + 
               "LTF_VERT: " + String(LTF_PWM) + ", " + 
               "RTB_VERT: " + String(RTB_PWM) + ", " +
               "LTB_VERT: " + String(LTB_PWM) + ", " +
               "servo: " + String(servo) + 
              String(depthSensor.depth()));

    LBF_T.writeMicroseconds(LBF_PWM);
    LBB_T.writeMicroseconds(LBB_PWM);
    RBF_T.writeMicroseconds(RBF_PWM);
    RBB_T.writeMicroseconds(RBB_PWM);    
    RTF_T.writeMicroseconds(RTF_PWM);
    LTF_T.writeMicroseconds(LTF_PWM);
    RTB_T.writeMicroseconds(RTB_PWM);
    LTB_T.writeMicroseconds(LTB_PWM);

    claw.write(pos);
    // Serial.println("Servo out of Loop: " + servo);
    // pos += 10*servo;
    if (servo != 0)
    {
      // Serial.println("Servo in Loop: " + servo);
      pos = 180;
    }
    else
    {
      pos = 0;
    }

    
    delay(5);
  }
}
