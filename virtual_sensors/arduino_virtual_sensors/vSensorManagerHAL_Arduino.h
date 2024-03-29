/*
 * vSensorManagerHAL_Arduino.h
 *
 *  Created on: 29.03.2018
 *      Author: User
 */

#ifndef VSENSORMANAGERHAL_ARDUINO_H_
#define VSENSORMANAGERHAL_ARDUINO_H_

//GPIO functions
void vSensorManager_setPinInterrupt(int pin);
void vSensorManager_setPinDirection(char* pin, int dir);
void vSensorManager_setPinState(char* pin, int state);
int vSensorManager_getPinState(char* pin);

//GPIO functions
void vSensorManager_setI2C();
void vSensorManager_joinI2C(int addr);



#endif /* VSENSORMANAGERHAL_ARDUINO_H_ */
