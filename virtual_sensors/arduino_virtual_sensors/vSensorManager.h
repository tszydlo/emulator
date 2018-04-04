/*
 * vSensorManager.h
 *
 *  Created on: 24.03.2018
 *      Author: User
 */

#ifndef VSENSORMANAGER_H_
#define VSENSORMANAGER_H_

//#include "vBME280.h"
//#include "vGPIOS.h"
//#include "vGPIO.h"
//#include "vLM35.h"
#include "vSensorTools.h"

//for arduino board only!
#include "vSensorManagerHAL_Arduino.h"


#ifdef __cplusplus
extern "C" {
#endif

//Provides few types of sensors:
// - BME280
// - LM35
// - GPIO
//For platforms:
// - arduino

#define vGPIO_PINS			10
#define vSENSOR_MAX			20
#define vSENSOR_VERSION		"V|0.1 alpha"

#define vSENSOR_GPIO_INPUT	0
#define vSENSOR_GPIO_OUTPUT	1

#define vSENSOR_GPIO_ON		0
#define vSENSOR_GPIO_OFF	1

#define vSENSOR_MAX	20


#define ARDUINO
#define HAL_MOCK


typedef struct {
	//table with GPIO pins for interrupts
	void* gpio_objects[vGPIO_PINS];
	void (*gpio_callbacks[vGPIO_PINS])(void*, int);

	//DAC

	//I2C

	//sensors - message processors
	//tablica wskaznikow do funkcji
	void (*sensor_message_processors_fun[vSENSOR_MAX])(void *, char*);
	void* sensors_object_types[vSENSOR_MAX];

	//function that forwards messages to emulator
	void (*fun_forwarder)(char*);
} vSensorManager_t;

void vSensorManager_ProcessMessage(vSensorManager_t* vSensorManager, char* message);
void vSensorManager_set_forwarder(vSensorManager_t* vSensorManager, void (*fun_forwarder)(char*));

#ifdef __cplusplus
} // extern "C"
#endif

#endif /* VSENSORMANAGER_H_ */
