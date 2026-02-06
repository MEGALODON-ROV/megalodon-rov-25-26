#include <Arduino.h>
#include "accelerometerTesting.h"

// put function declarations here:
// int myFunction(int, int);

void setup() {
  // put your setup code here, to run once:
  initializeMPU();
}

void loop() {
  // put your main code here, to run repeatedly:
  readMPU();
}

// put function definitions here:
// int myFunction(int x, int y) {
//   return x + y;
// }