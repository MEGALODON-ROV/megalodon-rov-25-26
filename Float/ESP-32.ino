#include <vector>
#include <ESP32Servo.h>
#include <MS5837.h>
#include <Wire.h>

int elapsedTime = 0;

const int SCLpin = 21;
const int SDApin = 22;
MS5837 sensor;

double depth = 0; // in meters
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
  Wire.begin(21, 22);  // SDA, SCL
  Serial.println("Initializing Depth Sensor...");

  while (!sensor.init()) {
    Serial.println("Init failed!");
    Serial.println("Are SDA/SCL connected correctly?");
    Serial.println("Blue Robotics Bar02: White=SDA, Green=SCL");
    Serial.println("\n\n\n");
    delay(1000);
  }


  sensor.setModel(MS5837::MS5837_30BA); // try 02BA if this doesn't work
  sensor.setFluidDensity(997); // freshwater
  Serial.println("Sensor ready!");

  Serial.println("Success!\n");

  delay(500);
}

// reads depth from pressure sensor
void getDepth() {
  sensor.read();
  depth = (double) sensor.depth();  // float -> double
  //depth -= baselineDepth;
}

void transmitData(){
  linearServo.writeMicroseconds(600);
  //insert code here
}

void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("Started Serial");
  initDepthSensor();
  linearServo.attach(17);    // pin 17
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