// #include <heltec.h>

#include "Arduino.h"
#include "WiFi.h"
#include "LoRaWan_APP.h"
#include <Wire.h>  
#include "HT_SSD1306Wire.h"
#include "MS5837.h"

#define TCAADDR 0x70
/********************************* lora  *********************************************/
#define RF_FREQUENCY                                868000000 // Hz

#define TX_OUTPUT_POWER                             10        // dBm

#define LORA_BANDWIDTH                              0         // [0: 125 kHz,
                                                              //  1: 250 kHz,
                                                              //  2: 500 kHz,
                                                              //  3: Reserved]
#define LORA_SPREADING_FACTOR                       7         // [SF7..SF12]
#define LORA_CODINGRATE                             1         // [1: 4/5,
                                                              //  2: 4/6,
                                                              //  3: 4/7,
                                                              //  4: 4/8]
#define LORA_PREAMBLE_LENGTH                        8         // Same for Tx and Rx
#define LORA_SYMBOL_TIMEOUT                         0         // Symbols
#define LORA_FIX_LENGTH_PAYLOAD_ON                  false
#define LORA_IQ_INVERSION_ON                        false


#define RX_TIMEOUT_VALUE                            1000
#define BUFFER_SIZE                                 30 // Define the payload size here

char txpacket[BUFFER_SIZE];
char rxpacket[BUFFER_SIZE];

static RadioEvents_t RadioEvents;
void OnTxDone( void );
void OnTxTimeout( void );
void OnRxDone( uint8_t *payload, uint16_t size, int16_t rssi, int8_t snr );

typedef enum
{
    LOWPOWER,
    STATE_RX,
    STATE_TX
} States_t;

const int SCLpin = 41;
const int SDApin = 42;

MS5837 depthSensor;
double depth; // in meters


int16_t txNumber;
int16_t rxNumber;
States_t state;
bool sleepMode = false;
int16_t Rssi,rxSize;

// String testnumber = "";
int value1 = 0;
int value2 = 0;

String rssi = "RSSI --";
String packSize = "--";
String packet;
String send_num;
String show_lora = "lora data show";

unsigned int counter = 0;
bool receiveflag = false; // software flag for LoRa receiver, received data makes it true.
long lastSendTime = 0;        // last send time
int interval = 1000;          // interval between sends
uint64_t chipid;
int16_t RssiDetection = 0;

unsigned long elapsedTime;
int seconds = 0;
int minutes = 0;
int x = 0;

int ArrayLength; //The +1 is for the 0x00h Terminator
char txpacketArray; //[ArrayLength];
//S.toCharArray(txpacketArray, ArrayLength);

String companyNumber = "RN05,";
String totalTimeElapsed = "";
String depthString = "";
String dataPacket = "";

void OnTxDone( void )
{
  //Serial.print("TX done......");
  state=STATE_RX;

}

void OnTxTimeout( void )
{
  Radio.Sleep( );
  Serial.print("TX Timeout......");
  state=STATE_TX;
}

void OnRxDone( uint8_t *payload, uint16_t size, int16_t rssi, int8_t snr )
{
  rxNumber++;
  Rssi=rssi;
  rxSize=size;
  memcpy(rxpacket, payload, size);
  rxpacket[size]='\0';
  Radio.Sleep( );
  //Serial.printf("\r\nreceived packet \"%s\" with Rssi %d , length %d\r\n",rxpacket,Rssi,rxSize);
  //Serial.println("wait to send next packet");
  receiveflag = true;
  state=STATE_TX;
}


void lora_init(void)
{
  Mcu.begin(HELTEC_BOARD,SLOW_CLK_TPYE);
  txNumber=0;
  Rssi=0;
  rxNumber = 0;
  RadioEvents.TxDone = OnTxDone;
  RadioEvents.TxTimeout = OnTxTimeout;
  RadioEvents.RxDone = OnRxDone;

  Radio.Init( &RadioEvents );
  Radio.SetChannel( RF_FREQUENCY );
  Radio.SetTxConfig( MODEM_LORA, TX_OUTPUT_POWER, 0, LORA_BANDWIDTH,
                                 LORA_SPREADING_FACTOR, LORA_CODINGRATE,
                                 LORA_PREAMBLE_LENGTH, LORA_FIX_LENGTH_PAYLOAD_ON,
                                 true, 0, 0, LORA_IQ_INVERSION_ON, 3000 );

  Radio.SetRxConfig( MODEM_LORA, LORA_BANDWIDTH, LORA_SPREADING_FACTOR,
                                 LORA_CODINGRATE, 0, LORA_PREAMBLE_LENGTH,
                                 LORA_SYMBOL_TIMEOUT, LORA_FIX_LENGTH_PAYLOAD_ON,
                                 0, true, 0, 0, LORA_IQ_INVERSION_ON, true );
  state=STATE_TX;
}


/********************************* lora  *********************************************/

SSD1306Wire  factory_display(0x3c, 500000, SDA_OLED, SCL_OLED, GEOMETRY_128_64, RST_OLED); // addr , freq , i2c group , resolution , rst

void WIFISetUp(void)
{
  // Set WiFi to station mode and disconnect from an AP if it was previously connected
  WiFi.disconnect(true);
  delay(100);
  WiFi.mode(WIFI_STA);
  WiFi.setAutoReconnect(true);
  WiFi.begin("Your WiFi SSID","Your Password");//fill in "Your WiFi SSID","Your Password"
  delay(100);

  byte count = 0;
  while(WiFi.status() != WL_CONNECTED && count < 10)
  {
    count ++;
    delay(500);
    factory_display.drawString(0, 0, "Connecting...");
    factory_display.display();
  }

  factory_display.clear();
  if(WiFi.status() == WL_CONNECTED)
  {
    factory_display.drawString(0, 0, "Connecting...OK.");
    factory_display.display();
//    delay(500);
  }
  else
  {
    factory_display.clear();
    factory_display.drawString(0, 0, "Connecting...Failed");
    factory_display.display();
    //while(1);
  }
  factory_display.drawString(0, 10, "WIFI Setup done");
  factory_display.display();
  delay(500);
}

void WIFIScan(unsigned int value)
{
  unsigned int i;
    WiFi.mode(WIFI_STA);

  for(i=0;i<value;i++)
  {
    factory_display.drawString(0, 20, "Scan start...");
    factory_display.display();

    int n = WiFi.scanNetworks();
    factory_display.drawString(0, 30, "Scan done");
    factory_display.display();
    delay(500);
    factory_display.clear();

    if (n == 0)
    {
      factory_display.clear();
      factory_display.drawString(0, 0, "no network found");
      factory_display.display();
      //while(1);
    }
    else
    {
      factory_display.drawString(0, 0, (String)n);
      factory_display.drawString(14, 0, "networks found:");
      factory_display.display();
      delay(500);

      for (int i = 0; i < n; ++i) {
      // Print SSID and RSSI for each network found
        factory_display.drawString(0, (i+1)*9,(String)(i + 1));
        factory_display.drawString(6, (i+1)*9, ":");
        factory_display.drawString(12,(i+1)*9, (String)(WiFi.SSID(i)));
        factory_display.drawString(90,(i+1)*9, " (");
        factory_display.drawString(98,(i+1)*9, (String)(WiFi.RSSI(i)));
        factory_display.drawString(114,(i+1)*9, ")");
        //factory_display.println((WiFi.encryptionType(i) == WIFI_AUTH_OPEN)?" ":"*");
        delay(10);
      }
    }

    factory_display.display();
    delay(800);
    factory_display.clear();
  }
}

bool resendflag=false;
bool deepsleepflag=false;
bool interrupt_flag = false;
void interrupt_GPIO0()
{
  interrupt_flag = true;
}
void interrupt_handle(void)
{
  if(interrupt_flag)
  {
    interrupt_flag = false;
    if(digitalRead(0)==0)
    {
      if(rxNumber <=2)
      {
        resendflag=true;
      }
      else
      {
        deepsleepflag=true;
      }
    }
  }

}
void VextON(void)
{
  pinMode(Vext,OUTPUT);
  digitalWrite(Vext, LOW);
  
}

void VextOFF(void) //Vext default OFF
{
  pinMode(Vext,OUTPUT);
  digitalWrite(Vext, HIGH);
}
void setup()
{
  Serial.begin(115200);
  Wire.begin(SDApin, SCLpin); //SDApin, SCLpin
  initDepthSensor();

  VextON();
  delay(100);
  factory_display.init();
  factory_display.clear();
  factory_display.display();
  delay(300);
  factory_display.clear();

  WIFISetUp();
  WiFi.disconnect(); //
  WiFi.mode(WIFI_STA);
  delay(100);

  WIFIScan(1);

  chipid=ESP.getEfuseMac();//The chip ID is essentially its MAC address(length: 6 bytes).
  Serial.printf("ESP32ChipID=%04X",(uint16_t)(chipid>>32));//print High 2 bytes
  Serial.printf("%08X\n",(uint32_t)chipid);//print Low 4bytes.

  attachInterrupt(0,interrupt_GPIO0,FALLING);
  lora_init();
  packet ="waiting lora data!";
  factory_display.drawString(0, 10, packet);
  factory_display.display();
  delay(100);
  factory_display.clear();
  pinMode(LED ,OUTPUT);
  digitalWrite(LED, LOW);

  delay(1000);
}


void loop()
{

interrupt_handle();
 if(deepsleepflag)
 {
  VextOFF();
  Radio.Sleep();
  SPI.end();
  pinMode(RADIO_DIO_1,ANALOG);
  pinMode(RADIO_NSS,ANALOG);
  pinMode(RADIO_RESET,ANALOG);
  pinMode(RADIO_BUSY,ANALOG);
  pinMode(LORA_CLK,ANALOG);
  pinMode(LORA_MISO,ANALOG);
  pinMode(LORA_MOSI,ANALOG);
  esp_sleep_enable_timer_wakeup(600*1000*(uint64_t)1000);
  esp_deep_sleep_start();

 }

 if(resendflag)
 {
  state = STATE_TX;
  resendflag = false;
 }

 if(receiveflag && (state==LOWPOWER) )
{
  receiveflag = false;
  packet ="R_data:";
  int i = 0;
  while(i < rxSize)
  {
    packet += rxpacket[i];
    i++;
  }
  //reset string
  totalTimeElapsed = "";
  depthString = "";
  dataPacket = "";

  // testnumber += packet;
  packSize = "R_Size: ";
  packSize += String(rxSize,DEC);
  packSize += " R_rssi: ";
  packSize += String(Rssi,DEC);
  //send_num = "send num: ";
  send_num = dataPacket;
  send_num += String(txNumber,DEC);
  factory_display.drawString(0, 0, show_lora);
  factory_display.drawString(0, 10, packet);
  factory_display.drawString(0, 20, packSize);
  factory_display.drawString(0, 50, send_num);
  factory_display.display();
  delay(10);
  factory_display.clear();

  if((rxNumber%2)==0)
  {
   digitalWrite(LED, HIGH);  
  }

  //parse the R_data for only the number
  // value1 = testnumber.indexOf(":");
  // value2 = testnumber.indexOf(",");
  // String newString = testnumber.substring(value1 + 1, value2);

  // Serial.println("testNumber:" + newString);
  // testnumber = "";
  
  //sofia's awesome time code
  elapsedTime = millis();
  seconds = (int)((int)elapsedTime/1000);
  minutes = (int)(seconds/60);
  seconds %= 60;  
  totalTimeElapsed += "Time:";
  //totalTimeElapsed += "00:";
  if (minutes < 10) {
    totalTimeElapsed += "0";
  }
  totalTimeElapsed += String(minutes);
  totalTimeElapsed += ":";
  if (seconds < 10) {
    totalTimeElapsed += "0";
  }
  totalTimeElapsed += String(seconds) + ",";
  
  //start depth collecting
  getDepth();
  depthString += "Depth:" + String(depth) + ",";

  dataPacket += companyNumber + totalTimeElapsed + depthString;
  //Serial.println(dataPacket);

  ArrayLength = dataPacket.length() + 1;
  // txpacketArray[ArrayLength];
}


String helloe12 = "23123";

switch(state)
  {
    case STATE_TX: 
      delay(1000);
      txNumber++;
      Serial.print("Data packet before transmission: " + dataPacket);
      sprintf(txpacket, dataPacket.c_str());
      //sprintf(txpacket,"hello %d,Rssi:%d",txNumber,Rssi);
      Serial.printf("\r\nsending packet \"%s\" , length %d\r\n\n",txpacket, strlen(txpacket));
      //Serial.println("");

      Radio.Send( (uint8_t *)txpacket, strlen(txpacket) );
      state=LOWPOWER;
      break;
    case STATE_RX:
      //Serial.println("into RX mode");
      Radio.Rx( 0 );
      state=LOWPOWER;
      break;
    case LOWPOWER:
      Radio.IrqProcess( );
      break;
    default:
      break;
  }
}

// intialize pressure sensor with necessary delays
void initDepthSensor() {
  delay(500);

  Serial.println("Intializing Depth Sensor...");

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
