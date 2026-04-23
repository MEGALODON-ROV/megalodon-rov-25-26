#include <Wire.h>
#include <Servo.h>
#include "MS5837.h"
#define TCAADDR 0x70

MS5837 depthSensor;
const int MPU_addr1 = 0x68;
float xAccel, yAccel, zAccel, roll, pitch;
double proportionalGain, integralGain, derivativeGain;
double error, derivativeError, previousError, integralSum, pidOutput;
double proportion_value, integral_value, derivative_value;
double depth, goal, depth_diff; // in meters
double bot_width = 17; //in inches
double baselineDepth, baselineRoll, baselinePitch;

int RBB_PWM;
int LBF_PWM;
int LBB_PWM;
int RBF_PWM;
int RTF_PWM;
int LTF_PWM;
int LTB_PWM;
int RTB_PWM;

int pos;
int servo;

Servo LBF_T; //left RBFont
Servo LBB_T; //left back
Servo RBF_T; //right RBFont
Servo RBB_T; //right back
Servo RTF_T;
Servo LTF_T;
Servo LTB_T;
Servo RTB_T;

Servo claw;

//Pid calculations :)
double PID(double depth, double goal) {
  int pidOutput;
  error = goal - depth; //depth RBFom sensor
  integralSum += error;
  //derivativeError = error - previousError;

  proportion_value = proportionalGain * error;
  //integral_value = integralGain * integralSum;
  //derivative_value = derivativeGain * derivativeError;

  pidOutput = proportion_value + integral_value + derivative_value;
  pidOutput = pidOutput;

  if (pidOutput > 0) {
    pidOutput += 36;
  }
  else {
    pidOutput -= 36;
  }

  pidOutput = max(-400, pidOutput);
  pidOutput = min(400, pidOutput);

  //previousError = error; //for derivative

  return pidOutput;
}

void setup() {
  Serial.begin(9600);
  Wire.begin();

  LBF_T.attach(4); //
  RBB_T.attach(11); //
  LBB_T.attach(8); //
  RBF_T.attach(6); //

  RTF_T.attach(7);
  LTF_T.attach(9);
  LTB_T.attach(5); //
  RTB_T.attach(3); // 3.1 back, 2.8 forward

  claw.attach(4);

  initDepthSensor(7);
  calibrateDepth();
  
  initMPU(1);
  calibrateMPU();

  tunePID(500, 10, 0);

  delay(1000);
}

int tick = 0;
int line = 0;

void loop() {
  if (Serial.available()) {
    line++;
    Serial.print("line ");
    Serial.print(line);
    RBF_PWM = Serial.readStringUntil('-').toInt();
    LBF_PWM = Serial.readStringUntil('=').toInt();
    RBB_PWM = Serial.readStringUntil('+').toInt();
    LBB_PWM = ((Serial.readStringUntil('*').toInt() - 1500) * (-1)) + 1500;
    RTF_PWM = Serial.readStringUntil(',').toInt();
    LTF_PWM = Serial.readStringUntil(']').toInt();
    RTB_PWM = Serial.readStringUntil('/').toInt();
    LTB_PWM = Serial.readStringUntil('.').toInt();
    servo = Serial.readStringUntil('!').toInt();
    
    

    if ((RTF_PWM > 1464) && (RTF_PWM < 1536)) {
      getDepth(7);
      // getAngle(1);

      Serial.print(" PID ON ");
      Serial.print("DEPTH: ");
      Serial.print(depth);
      Serial.print(" ");
      
//      Serial.print("Depth: ");
//      Serial.print(depth);
//      
//      Serial.print(" | Roll: ");
//      Serial.print(roll);
//      
//      Serial.print(" | Pitch: ");
//      Serial.println(pitch);
      
      // depth_diff = bot_width / (tan(roll - PI / 2)); // in inches
      // depth_diff /= 39.37; // conversion to meters
      
      // gets depth every 50 readings to ensure it stays in place
      if (tick == 0) {
        goal = depth;
        tick++;
      }
      else if (tick == 100) {
        tick = 0;
      }
      
      

      int pidPWM = PID(depth, goal);
      Serial.print("PiDPWM: ");
      Serial.print(pidPWM);
    
      RTF_PWM += PID(depth, goal);
      LTF_PWM += PID(depth, goal);
      LTB_PWM += PID(depth, goal);
      RTB_PWM += PID(depth, goal);
      Serial.print("tick: ");
      Serial.print(tick);
    }
    else {
      tick = 0;
    }    

    depthSensor.read()
    Serial.println(
               "RBF_PWM: " + String(RBF_PWM) + ", " + 
               "LBF_PWM: " + String(LBF_PWM) + ", " + 
               "RBB_PWM: " + String((RBB_PWM - 1500) * (-1) + 1500) +
               "LBB_PWM: " + String(LBB_PWM) + ", " + 
               "RTF_VERT: " + String(RTF_PWM) + ", " + 
               "LTF_VERT: " + String(LTF_PWM) + ", " + 
               "LTB_VERT: " + String(LTB_PWM) + ", " +
               "RTB_VERT: " + String(RTB_PWM) + "; " +
               String(depthSensor.depth()));

    LBF_T.writeMicroseconds(LBF_PWM);
    LBB_T.writeMicroseconds(LBB_PWM);
    RBF_T.writeMicroseconds(RBF_PWM);
    RBB_T.writeMicroseconds(RBB_PWM);    
    RTF_T.writeMicroseconds(RTF_PWM);
    LTF_T.writeMicroseconds(LTF_PWM);
    LTB_T.writeMicroseconds(LTB_PWM);
    RTB_T.writeMicroseconds(RTB_PWM);

    claw.write(pos);
    if (servo != 0)
    {
      pos = 360;
    }
    else
    {
      pos = -180;
    }

//    Serial.println("RB_PWM: " + String((RB_PWM - 1500) * (-1) + 1500) + ", " +
//                   "LF_PWM: " + String(LF_PWM) + ", " + 
//                   "LB_PWM: " + String(LB_PWM) + ", " + 
//                   "RF_PWM: " + String(RF_PWM) + ", " + 
//                   "RBFONT_VERT: " + String(RBFONT_PWM) + ", " + 
//                   "BACK_VERT: " + String(BACK_PWM));
    
    // delay(10);
  }
}





// change SDA/SCL on mux
void selectChannel(int channel) {
  if (channel > 7) return;

  Wire.beginTransmission(0x70); // TCA9548A address
  Wire.write(1 << channel);     // send byte to select bus
  Wire.endTransmission();
}


// intialize pressure sensor with necessary delays
void initDepthSensor(int channel) {
  delay(500);

  Serial.println("Intializing Depth Sensor...");
  selectChannel(channel);

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


// intialize MPU6050 with necessary delays
void initMPU(int channel) {
  delay(500);
  Serial.println("Intializing MPU6050...");

  selectChannel(channel);
  Wire.beginTransmission(MPU_addr1);                 //begin, send the slave adress (in this case 68)
  Wire.write(0x6B);                                  //make the reset (place a 0 into the 6B register)
  Wire.write(0);
  Wire.endTransmission(true);                        //end the transmission

  Serial.println("Success!\n");
  delay(500);
}


// reads depth RBFom pressure sensor
void getDepth(int channel) {
  selectChannel(channel);
  depthSensor.read();
  depth = (double) depthSensor.depth();  // LBFoat -> double
  depth -= baselineDepth;
}


// MPU6050 calculations to obtain roll and pitch
void getAngle(int channel) {
  selectChannel(channel);

  Wire.beginTransmission(MPU_addr1);
  Wire.write(0x3B);  //send starting register address, accelerometer high byte
  Wire.endTransmission(false); //restart for read

  Wire.requestFrom(MPU_addr1, 6, true); //get six bytes accelerometer data
  int t = Wire.read();
  xAccel = (t << 8) | Wire.read();
  t = Wire.read();
  yAccel = (t << 8) | Wire.read();
  t = Wire.read();
  zAccel = (t << 8) | Wire.read();

  // IN RADIANS
  roll = atan2(yAccel , zAccel);
  pitch = atan2(-xAccel , sqrt(yAccel * yAccel + zAccel * zAccel)); //account for roll already applied
  
  
  // convert to degrees
  // roll *= 180.0 / PI;
  // pitch *= 180.0 / PI;

  roll -= baselineRoll;
  pitch -= baselinePitch;

}





//change gain values
void tunePID(double proportional, double integral, double derivative) {
  proportionalGain = proportional;
  integralGain = integral;
  derivativeGain = derivative;
}


void calibrateDepth() {
  Serial.println("Calibrating Depth Sensor");
  
  int tick1 = 0;
  double sum = 0.0;
  while (tick1 < 100) {
    getDepth(7);
    sum += depth;
    
    tick1++;
  }

  baselineDepth = sum/tick1;

  Serial.print("Depth Deviation: ");
  Serial.println(baselineDepth);
  Serial.println();

  delay(300);
}


void calibrateMPU() {
  Serial.println("Calibrating MPU6050");
  
  int tick2 = 1;
  double rollSum = 0.0;
  double pitchSum = 0.0;
  
  while (tick2 <= 100) {
    getAngle(1);
    rollSum += roll;
    pitchSum += pitch;
    tick2++;
  }

  baselineRoll = rollSum/tick2;
  baselinePitch = pitchSum/tick2;

  Serial.print("Roll Deviation: ");
  Serial.println(baselineRoll);
  Serial.print("Pitch Deviation: ");
  Serial.println(baselinePitch);
  Serial.println();

  delay(300);
}
