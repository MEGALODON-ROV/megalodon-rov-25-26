#include "FS.h"
#include "SD.h"
#include <SPI.h>
#include "esp_system.h"

#define SD_SCK 18 //Serial clock
#define SD_MISO 19 //master in slave out
#define SD_MOSI 23 //master out slave in

const int sd_cs = 5;

int elapsedTime;

void listDir(fs::FS &fs, const char * dirname) {
  Serial.print("DIR ");
  Serial.println(dirname);

  File root = fs.open(dirname);
  if (!root || !root.isDirectory()) {
    Serial.println("open fail");
    return;
  }

  bool found = false;

  while (true) {
    File file = root.openNextFile();
    if (!file) break;

    found = true;

    if (file.isDirectory()) {
      Serial.print("D ");
      Serial.println(file.name());
    } else {
      Serial.print("F ");
      Serial.print(file.name());
      Serial.print(" ");
      Serial.println((uint32_t)file.size());
    }

    file.close();
  }

  if (!found) Serial.println("empty");

  root.close();
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

void testFileIO(fs::FS &fs, const char * path) {
  Serial.println("test IO");

  File file = fs.open(path);
  static uint8_t buf[512];

  if (file) {
    size_t len = file.size();
    Serial.print("size ");
    Serial.println((uint32_t)len);

    while (len) {
      size_t toRead = len > 512 ? 512 : len;
      file.read(buf, toRead);
      len -= toRead;
    }

    file.close();
  }

  file = fs.open(path, FILE_WRITE);
  if (!file) {
    Serial.println("write fail");
    return;
  }

  for (int i = 0; i < 2048; i++) {
    file.write(buf, 512);
  }

  file.close();
  Serial.println("1MB write done");
}

void setup() {
  Serial.end();
  Serial.begin(115200);
  delay(1000);
  Serial.print("reset ");
  Serial.println(esp_reset_reason());

  //Serial.println("SD start test 2");

  SPI.begin(SD_SCK, SD_MISO, SD_MOSI, sd_cs);

  if (!SD.begin(sd_cs)) {
    Serial.println("mount fail");
    return;
  }

  Serial.println("mounted");

  uint8_t cardType = SD.cardType();

  Serial.print("type ");
  if (cardType == CARD_SDHC) Serial.println("SDHC");
  else if (cardType == CARD_SD) Serial.println("SDSC");
  else if (cardType == CARD_MMC) Serial.println("MMC");
  else Serial.println("unk");

  uint32_t cardMB = SD.cardSize() / (1024 * 1024);

  Serial.print("sizeMB ");
  Serial.println(cardMB);

  uint32_t totalMB = SD.totalBytes() / (1024 * 1024);
  uint32_t usedMB  = SD.usedBytes() / (1024 * 1024);

  listDir(SD, "/");

  Serial.print("totalMB ");
  Serial.println(totalMB);

  Serial.print("usedMB ");
  Serial.println(usedMB);
}

void loop() {
}