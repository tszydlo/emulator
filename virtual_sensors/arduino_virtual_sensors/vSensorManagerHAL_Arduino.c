#include "vSensorManager.h"

#ifdef ARDUINO
#include "Arduino.h"

#include <stdio.h>
#include <stdlib.h>

////////////////////////////////////////////////////////
// GPIO //
////////////////////////////////////////////////////////
void vSensorArduinoINT0_PIN2() {
  //vSensorManager_PinNotification(2,state);
}

void vSensorArduinoINT1_PIN3() {
  //vSensorManager_PinNotification(3,state);
}

void vSensorManager_setPinInterrupt(int pin){
  //tutaj na arduino ustawiamy pin na ktorym ma byc wywolywane przerwanie
  //pinMode(interruptPin, INPUT_PULLUP);
  //attachInterrupt(digitalPinToInterrupt(interruptPin), blink, CHANGE);
}

// / / / / / / / / /
void vSensorManager_setPinDirection(char* pin, int dir){
	//tutaj na arduino ustawiamy kierunek pinow
	//pinMode(ledPin, OUTPUT);
	//pinMode(interruptPin, INPUT_PULLUP);

	//printf("ARDUINO PIN DIRECTION:%s:\n",pin);

	if (!vSensor_conditional_strcmp("PD13",pin)){
	    pinMode(13, OUTPUT);
	}
}

void vSensorManager_setPinState(char* pin, int state){
	//if (!vSensor_conditional_strcmp("PD13",pin)){
	//	digitalWrite(13, state);
	//}
	if (!vSensor_conditional_strcmp("PD13",pin)){
		digitalWrite(13, state);
	}
}

int vSensorManager_getPinState(char* pin){
	//if (!vSensor_conditional_strcmp("PD13",pin)){
	//	return digitalRead(13);
	//}
	if (!vSensor_conditional_strcmp("PD13",pin)){
	  return digitalRead(13);
	}
}

///////////////////////////////////////////////////////
// I2C //
///////////////////////////////////////////////////////
void vSensorManager_setI2C(){

}

void vSensorManager_joinI2C(int addr){

}

#endif
