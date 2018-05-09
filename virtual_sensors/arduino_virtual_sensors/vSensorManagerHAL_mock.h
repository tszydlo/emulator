/*
 * vSensorManagerHAL_mock.h
 *
 *  Created on: 09.05.2018
 *      Author: User
 */

#ifndef VSENSORMANAGERHAL_MOCK_H_
#define VSENSORMANAGERHAL_MOCK_H_

//GPIO functions
void vSensorManager_setPinInterrupt(int pin);
void vSensorManager_setPinDirection(char* pin, int dir);
void vSensorManager_setPinState(char* pin, int state);
int vSensorManager_getPinState(char* pin);

//GPIO functions
void vSensorManager_setI2C();
void vSensorManager_joinI2C(int addr);


#endif /* VSENSORMANAGERHAL_MOCK_H_ */
