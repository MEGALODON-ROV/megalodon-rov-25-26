void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);     // 2 speeds to send info (baud rate): 115,200 and 9600
}


void loop() {
  // put your main code here, to run repeatedly:
  Serial.println("Hello World :)");
}