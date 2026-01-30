// constants won't change. "Const" means that the variables won't change
const int IN1_PIN = 6; // the Arduino pin connected to the IN1 pin L298N
const int IN2_PIN = 5; // the Arduino pin connected to the IN2 pin L298N

// the setup function runs once when you press reset or power the board
void setup() { //setup runs ONLY once
  Serial.begin(9600);
  // initialize digital pins as outputs.
  pinMode(IN1_PIN, OUTPUT); 
  pinMode(IN2_PIN, OUTPUT);

  initActuator();

  delay(100);
//basically this is saying that on the Arduino the pins 5 and 6 are going to //act as Output pins. This is because we are outputting a signal to the In1 and In2 pins on the H-bridge. This is opposed to an input pin where the Arduino would be reading data or something
}


void loop() { // the loop function runs over and over again forever
  completeCycle();
}
  
  

  // if (input1.equals("hi")) {
  //   Serial.println("command received");
  // }

  //Serial.println("no");

  




void completeCycle() {


  // retract the actuator (float goes down)
  Serial.println("Retracting Linear Actuator...");
  digitalWrite(IN1_PIN, LOW); //digitalWrite basically 
  digitalWrite(IN2_PIN, HIGH);

  delay(60000);

  Serial.print("Stagnant");
  digitalWrite(IN1_PIN, LOW); //lower and upper cases for the HIGH and LOW don't matter
  digitalWrite(IN2_PIN, LOW); 

  delay(10000);

  // extend the actuator (float goes up) -- takes 38 seconds, rounded to 40
  Serial.println("Extending Linear Actuator...");
  digitalWrite(IN1_PIN, HIGH); //lower and upper cases for the HIGH and LOW don't matter
  digitalWrite(IN2_PIN, LOW); 
  //basically these two lines are "reversing the polarity" (or direction) of the actuator

  delay(60000); // actuator will stop retracting automatically when reaching the limit

  Serial.print("Stagnant");
  digitalWrite(IN1_PIN, LOW); //lower and upper cases for the HIGH and LOW don't matter
  digitalWrite(IN2_PIN, LOW); 

  delay(10000);
  //delay(40000); // delay() stops the code for a while. This basically means that the actuator will just keep going according to the last two lines before the delay for 60 seconds. The function delay() uses microseconds (there are 1000 microseconds in one second). So delay(60000) means delay for 60 seconds. HOWEVER, the actuator stops before 60 (it fully extends or retracts by that point) so will stop extending automatically when reaching the limit. 

}

void initActuator() {
  Serial.println("Reseting Linear Actuator...\n");
    // retract the actuator (float goes down)
  digitalWrite(IN1_PIN, HIGH); //digitalWrite basically 
  digitalWrite(IN2_PIN, LOW);

  delay (45000);
}