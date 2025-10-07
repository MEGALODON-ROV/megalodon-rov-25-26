

void setup() {
  // put your setup code here, to run once:
  pinMode(13, OUTPUT);    // red light
  pinMode(9, OUTPUT);     // green light
  pinMode(3, OUTPUT);     // blue light
  pinMode(7, INPUT_PULLUP);    // button
}

void loop() {
  // put your main code here, to run repeatedly:
  /*
  // TURNING ON AND OFF
  digitalWrite(13, HIGH);   // sends signal to turn on pin 13 (LED)
  digitalWrite(9, LOW);
  analogWrite(3, 255);    // max brightness
  delay(500);
  digitalWrite(13, LOW);
  digitalWrite(9, HIGH);
  analogWrite(3, 2);     // dimmer
  delay(500);
  */
  /*
  // GRADUAL BRIGHTENING AND DIMMING
  for (int i = 0; i<=255; i++) {    // dim to bright
    analogWrite(3, i);
    delay(10);
  }
  for (int i = 255; i >= 0; i--) {    // bright to dim
    analogWrite(3, i);
    delay(10);
  }
  */

  // USING A BUTTON TO TURN ON THE LIGHT
  bool isPressed = !digitalRead(7);
  if (isPressed) {
    digitalWrite(13, HIGH);
  }
  else {
    digitalWrite(13, LOW);
  }
}