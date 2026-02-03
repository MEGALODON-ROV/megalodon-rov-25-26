#include "vector"
#include "Servo.h"
#include "MS5837.h"

int elapsedTime = 0;

const int SCLpin = 41;
const int SDApin = 42;
MS5837 depthSensor;
double depth; // in meters
String depthString = "";
int targetAchievedTime = 0;
boolean targetAchieved = false;

Servo linearServo;
int currentIndex = 0;
int servoMin = 600;
int servoMax = 2300;
int servoCurrent = 1500;

servoCurrent = servoCurrent(servoCurrent, servoMin, servoMax);
double kP = 0; //change

struct ProfileStep {
    int profileNum;    
    double targetDepth; //in meters
};
std::vector<ProfileStep> profileTable = {
    {1, 2.5},
    {1, 0.4},
    {2, 2.5},
    {2, 0.4},
    {2, 0.0}
};

double currentDepth;
totalTimeElapsed = "";
depthString = "";
dataPacket = "";

// initialize pressure sensor with necessary delays
void initDepthSensor() {
  delay(500);

  Serial.println("Initializing Depth Sensor...");

  while (!depthSensor.init()) {
    Serial.println("Init failed!");
    Serial.println("Are SDA/SCL connected correctly?");
    Serial.println("Blue Robotics Bar02: White=SDA, Green=SCL");
    Serial.println("\n\n\n");
    delay(5000);
  }

  depthSensor.setModel(MS5837::MS5837_02BA);
  depthSensor.setFluidDensity(997);
  depthSensor.init();

  Serial.println("Success!\n");

  delay(500);
}

// reads depth from pressure sensor
void getDepth() {
  depthSensor.read();
  depth = (double) depthSensor.depth();  // float -> double
  //depth -= baselineDepth;
}

void setup() {
  linearServo.attach(9);    // MEGA pin 9
  initDepthSensor();
}

void loop() {
  elapsedTime = millis();

  // put your main code here, to run repeatedly:
  current = current + (goalDepth - currentDepth) * kP;
  linearServo.writeMicroseconds(current);
  
  if (depth < profileTable[i].targetDepth + 0.3 && depth > profileTable[i].targetDepth - 0.3 )
  {
    targetAchieved = true;
    targetAchievedTime = millis();
  }
  if ((currentTime-targetAchievedTime >=30000) && !(targetAchieved)) {
    targetAchieved = false;
    currentIndex++;
  }



  //start depth collecting
  getDepth();
  depthString += "Depth:" + String(depth) + ",";

  dataPacket += companyNumber + totalTimeElapsed + depthString;
  Serial.println(dataPacket);

}