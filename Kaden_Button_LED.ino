void setup() {
  // put your setup code here, to run once:
  pinMode(11, OUTPUT);
  pinMode(8,INPUT_PULLUP);
}

void loop() {
  // put your main code here, to run repeat
 // digitalWrite(13, LOW);
  bool pressed = digitalRead(8);
  if (!pressed){
   digitalWrite(11,HIGH);
  }
  else{
   digitalWrite(11,LOW); 
  }
}
