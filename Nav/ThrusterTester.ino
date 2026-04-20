
#include <Servo.h>


Servo LBF_T; // yellow
Servo RBB_T; // black
Servo LBB_T; // green
Servo RBF_T; // grey

Servo RTF_T; // dark purple (purple not connected to gnd)
Servo LTF_T; // white
Servo LTB_T; // orange
Servo RTB_T;

Servo claw;

// lbf, rbb, lbb, rbf, rtf, ltf, ltb, rtb 

Servo thrusterInit[8] = {LBF_T, RBB_T, LBB_T, RBF_T, RTF_T, LTF_T, LTB_T, RTB_T};

boolean test = true;


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

  for (int i = 0; i < 8; i++)
  {
    thrusterInit[i].writeMicroseconds(1500);
  }

  // MAY NEED TO UNCOMMENT THIS IF NO WORK

  // LBF_T.writeMicroseconds(1500); // yellow
  // RBB_T.writeMicroseconds(1500); // black
  // LBB_T.writeMicroseconds(1500); // green
  // RBF_T.writeMicroseconds(1500); // grey

  // RTF_T.writeMicroseconds(1500); // dark purple (purple not connected to gnd)
  // LTF_T.writeMicroseconds(1500); // white
  // LTB_T.writeMicroseconds(1500); // orange
  // RTB_T.writeMicroseconds(1500); // blue

  claw.write(0);

  
  delay(7000);
}


void loop()
{

  
  if (test)
  {
    Servo Thrusters[8] = {LBF_T, RBB_T, LBB_T, RBF_T, RTF_T, LTF_T, LTB_T, RTB_T};
    String thrusterNames[8] = {"LBF_T", "RBB_T", "LBB_T", "RBF_T", "RTF_T", "LTF_T", "LTB_T", "RTB_T"};

    // testAll(Thrusters);
    testEach(Thrusters, thrusterNames);
    test = false;
  }
}


void testAll(Servo Thrusters[])
{

  for (int i = 0; i < 8; i++)
  {
    Thrusters[i].writeMicroseconds(1600);
  }

  delay(2500);

  for (int i = 0; i < 8; i++)
  {
    Thrusters[i].writeMicroseconds(1500);
  }
}


void testEach(Servo Thrusters[], String thrusterNames[])
{
  for (int i = 0; i < 8; i++)
  {
    Servo thruster = Thrusters[i];
    String name = thrusterNames[i];

    Serial.println("Now Testing " + name);
    thruster.writeMicroseconds(1600);
    delay(2500);
    thruster.writeMicroseconds(1500);
    delay(500);
  }

}

void testClaw()
{
  claw.write(360);
  delay(1000);
  claw.write(0);
}
