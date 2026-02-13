#include <vector>
#include <ESP32Servo.h>
#include <MS5837.h>
#include <Wire.h>

int elapsedTime = 0;

const int SCLpin = 21;
const int SDApin = 22;
MS5837 depthSensor;
double depth; // in meters
String depthString = "";
String dataPacket = "";
int targetAchievedTime = 0;
boolean targetAchieved = false;

Servo linearServo;
int currentIndex = 0;
int servoMin = 600;
int servoMax = 2300;
int servoCurrent = 1500;

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

void transmitData(){
  linearServo.writeMicroseconds(600);
  //insert code here
}

void setup() {
  Serial.begin(115200);
  Wire.begin(SDApin, SCLpin);
  linearServo.attach(17);    // pin 17
  initDepthSensor();
}

void loop() {
  if (currentIndex > profileTable.size() - 1) {
    transmitData();
  } else {
    servoCurrent = constrain(servoCurrent, servoMin, servoMax);

    elapsedTime = millis();

    // put your main code here, to run repeatedly:
    if (abs(profileTable[currentIndex].targetDepth - depth) > 0.05) {
      servoCurrent = 1500 + (profileTable[currentIndex].targetDepth - depth) * kP;
    }

    linearServo.writeMicroseconds(servoCurrent);
    
    if (depth < profileTable[currentIndex].targetDepth + 0.3 && depth > profileTable[currentIndex].targetDepth - 0.3 )
    {
      targetAchieved = true;
      targetAchievedTime = millis();
    }
    if ((elapsedTime-targetAchievedTime >=30000) && (targetAchieved)) {
      targetAchieved = false;
      currentIndex++;
    }

    //start depth collecting
    getDepth();
    depthString += "Depth:" + String(depth) + ",";

    //dataPacket += companyNumber + totalTimeElapsed + depthString;

    Serial.println(dataPacket);
    dataPacket = "";
    depthString = "";
  }
}