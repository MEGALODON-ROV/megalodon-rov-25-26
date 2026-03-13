#include <vector>
#include <ESP32Servo.h>
#include <MS5837.h>
#include <Wire.h>
#include "FS.h"
#include "SD.h"
#include <SPI.h>
#include "esp_system.h"

int elapsedTime = 0;

const int SCLpin = 21;
const int SDApin = 22;
MS5837 sensor;

#define SD_SCK 18
#define SD_MISO 19
#define SD_MOSI 23

const int sd_cs = 5;

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

double kP = 130; //change

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


  sensor.setModel(MS5837::MS5837_02BA); // try 02BA if this doesn't work
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
  Serial.println("transmitting data");
  //insert code here
}

void writeFile(fs::FS &fs, const char * path, const char * msg) {
  Serial.print("write ");
  Serial.println(path);

  File file = fs.open(path, FILE_WRITE);
  if (!file) {
    Serial.println("open fail");
    return;
  }

  if (file.print(msg)) Serial.println("ok");
  else Serial.println("fail");

  file.close();
}

void readFile(fs::FS &fs, const char * path) {
  Serial.print("read ");
  Serial.println(path);

  File file = fs.open(path);
  if (!file) {
    Serial.println("open fail");
    return;
  }

  while (file.available()) {
    Serial.write(file.read());
  }
  Serial.println();

  file.close();
}

void appendFile(fs::FS &fs, const char * path, const char * msg) {
  Serial.print("append ");
  Serial.println(path);

  File file = fs.open(path, FILE_APPEND);
  if (!file) {
    Serial.println("open fail");
    return;
  }

  if (file.print(msg)) Serial.println("ok");
  else Serial.println("fail");

  file.close();
}

void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("Started Serial");
  initDepthSensor();
  linearServo.attach(17);    // pin 17

  SPI.begin(SD_SCK, SD_MISO, SD_MOSI, sd_cs);
  if (!SD.begin(sd_cs)) {
    Serial.println("mount fail");
  } else {
    Serial.println("mounted");
  }

    writeFile(SD, "/data_packet1.txt", "MEGALODON ROV DATA PACKET \n");
}

void loop() {
  if (currentIndex > profileTable.size() - 1) {
    transmitData();
  } else {

    elapsedTime = millis();

    // put your main code here, to run repeatedly:
    if (abs(profileTable[currentIndex].targetDepth - depth) > 0.05) {
      servoCurrent = 1500 + (profileTable[currentIndex].targetDepth - depth) * kP;
      if(servoCurrent < servoMin)
      {
        servoCurrent = 600;
      } else if (servoCurrent > servoMax)
      {
        servoCurrent = 2300;
      }
    }

    linearServo.writeMicroseconds(servoCurrent);
    
    if ((depth < profileTable[currentIndex].targetDepth + 0.3) && (depth > profileTable[currentIndex].targetDepth - 0.3) && (!targetAchieved))
    {
      targetAchieved = true;
      targetAchievedTime = millis();
    }
    if ((elapsedTime-targetAchievedTime >=30000) && (targetAchieved)) {
      targetAchieved = false;
      currentIndex++;
    }

    getDepth();

    dataPacket = "MEGALODON ROV \n" + "Time:" + elapsedTime + "Depth:" + String(depth) + ", servoCurrent: " + servoCurrent + ", targetDepth: " + profileTable[currentIndex].targetDepth;
    appendFile(SD, "/data_packet1.txt", dataPacket);
  }
}