#include "FS.h"
#include "SD.h"
#include <SPI.h>
#include "esp_system.h"

#define SD_SCK 18 //Serial clock
#define SD_MISO 19 //master in slave out
#define SD_MOSI 23 //master out slave in

void getData() {
  Serial.end();
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

  listDir(SD, "/");

  readFile(SD, "/data_packet1.txt");

  uint32_t totalMB = SD.totalBytes() / (1024 * 1024);
  uint32_t usedMB  = SD.usedBytes() / (1024 * 1024);

  Serial.print("totalMB ");
  Serial.println(totalMB);

  Serial.print("usedMB ");
  Serial.println(usedMB);
}