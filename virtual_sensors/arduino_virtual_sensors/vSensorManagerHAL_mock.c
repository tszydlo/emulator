#include "vSensorManager.h"

#ifdef MOCK

#include <stdio.h>
#include <stdlib.h>

////////////////////////////////////////////////////////
// GPIO //
////////////////////////////////////////////////////////
void vSensorManager_setPinInterrupt(int pin){
}

// / / / / / / / / /
void vSensorManager_setPinDirection(char* pin, int dir){
	printf("MOCK PIN DIRECTION:%s:\n",pin);
}

void vSensorManager_setPinState(char* pin, int state){
	printf("MOCK PIN SET STATE:%s:\n",pin);
}

int vSensorManager_getPinState(char* pin){
	printf("MOCK PIN GET STATE:%s:\n",pin);
	return 0;
}

///////////////////////////////////////////////////////
// I2C //
///////////////////////////////////////////////////////
void vSensorManager_setI2C(){

}

void vSensorManager_joinI2C(int addr){
	printf("MOCK JOIN I2C:%d:\n",addr);
}

#endif
