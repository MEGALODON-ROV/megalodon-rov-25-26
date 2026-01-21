void setup() {
  // put your setup code here, to run once:
  pinMode(6, OUTPUT);
  pinMode(8, INPUT_PULLUP);
  
}

void loop() {
  // put your main code here, to run repeatedly:
  
  // digitalRead //recieves 
  // analogWrite(6, 255);
  // delay(500);
  // analogWrite(6, 20);
  // // delay(500);
  // for (int i = 255; i >= 0; i--) {
  //   analogWrite(6, i);
  //   delay(20);
  // }
  // for (int i = 0; i <= 255; i++) {
  //   analogWrite(6, i);
  //   delay(20);


  // }
  bool input_button = !analogRead(8);
  if (input_button)
  {
    digitalWrite(6, HIGH);
  }
  else
  {
    digitalWrite(6, LOW);
  }




}
