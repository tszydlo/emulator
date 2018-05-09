
#include <Wire.h>
#include "vSensormanager.h"
//#include "vBME280.h"

uint8_t last_reg;


String inputString = "";         // a String to hold incoming data
boolean stringComplete = false;  // whether the string is complete


vSensorManager_t sensor_manager;

//vBME280_t sensor;

void message_forwarder(char* message){
  Serial.println(message);
}

void arduinoHAL_wire_begin(int addr){
  Wire.begin(addr);
}

void setup() {
  //vBME280_init(&sensor);
  //vBME280_setTemp(&sensor, 35.76);
  //vBME280_setHumidity(&sensor, 55.55);
  //vBME280_setPressure(&sensor, 100900.9);

  vSensorManager_set_forwarder(&sensor_manager, &message_forwarder);
  

  //Wire.begin(...) should be moved to vSensorManagerHAL_Arduino.c
  Wire.begin(0x77); // join i2c bus with address #0x77
  
  Wire.onReceive(receiveEvent); // register event
  Wire.onRequest(requestEvent);
  Serial.begin(38400);           // start serial for output
  // reserve 200 bytes for the inputString:
  inputString.reserve(200);
}

void loop() {
  //delay(100);
    // print the string when a newline arrives:
  if (stringComplete) {
    Serial.println(inputString);
    printf(">|%s|<\n", inputString.c_str());
    //Serial.println(inputString.c_str());
    vSensorManager_ProcessMessage(&sensor_manager, inputString.c_str());
    
    
    // clear the string:
    inputString = "";
    stringComplete = false;
  }
}


void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the inputString:
    // if the incoming character is a newline, set a flag so the main loop can
    // do something about it:
    if (inChar == '\n') {
      stringComplete = true;
    } else {
          inputString += inChar;
    }
  }
}


/////////////////I2C/////////////////////////

void requestEvent()
{
    //Wire.send(registerMap, REG_MAP_SIZE);  //Set the buffer up to send all 14 bytes of data
    //Wire.write(0x60);
    //Wire.write(vBME280_readRegister(&sensor,last_reg));
    //Wire.write(vBME280_readRegisters(&sensor,last_reg), vBME280_readRegisterSize(&sensor,last_reg));
    ////////Wire.write(vBME280_readRegisters(&sensor,last_reg), 30);

    Wire.write(vSensorManager_i2c_readRegisters(&sensor_manager,0x77,last_reg), 30);
    
    //Serial.println("REQUEST");
}

// function that executes whenever data is received from master
// this function is registered as an event, see setup()
void receiveEvent(int howMany) {
  while (1 < Wire.available()) { // loop through all but the last
    int c = Wire.read(); // receive byte as a character
    //Serial.print(c);         // print the character
    //Serial.print(" ");
  }
  int x = Wire.read();    // receive byte as an integer
  last_reg=x;
  //Serial.println(x);         // print the integer
}
