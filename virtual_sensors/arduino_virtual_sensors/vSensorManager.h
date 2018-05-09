/*
 * vSensorManager.h
 *
 *  Created on: 24.03.2018
 *      Author: User
 */

#ifndef VSENSORMANAGER_H_
#define VSENSORMANAGER_H_

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#define ARDUINO
//#define MOCK

#ifdef ARDUINO
//for arduino board only!
#include "vSensorManagerHAL_Arduino.h"
#else
#include "vSensorManagerHAL_mock.h"
#endif


#ifdef __cplusplus
extern "C" {
#endif

//Provides few types of sensors:
// - BME280
// - LM35
// - GPIO
//For platforms:
// - arduino

#define vGPIO_PINS			10	//max pin numbers
#define vSENSOR_MAX			20  //max number of sensors for the board
#define vSENSOR_VERSION		"V|0.1 alpha"

#define vSENSOR_GPIO_INPUT	0
#define vSENSOR_GPIO_OUTPUT	1

#define vSENSOR_GPIO_ON		0
#define vSENSOR_GPIO_OFF	1

#define vSENSOR_I2C_MAX	5	//max number of I2C sensors



typedef struct {
	//table with GPIO pins for interrupts
	void* gpio_objects[vGPIO_PINS];
	void (*gpio_callbacks[vGPIO_PINS])(void*, int);

	//I2C

	//tablica z numerami urzadzen I2C
	uint16_t i2c_vsensors_addresses[vSENSOR_I2C_MAX];
	uint16_t i2c_vsensors_id[vSENSOR_I2C_MAX];
	uint8_t i2c_vsensors_count;

	//tablice funkcji obs�ugi wirtualnych urz�dze� I2C
	uint8_t (*i2c_readRegister_fun[vSENSOR_I2C_MAX])(void* sensor, uint8_t reg);
	uint8_t* (*i2c_readRegisters_fun[vSENSOR_I2C_MAX])(void* sensor, uint8_t reg);
	uint8_t (*i2c_readRegisterSize_fun[vSENSOR_I2C_MAX])(void* sensor, uint8_t reg);
	void (*i2c_writeRegister_fun[vSENSOR_I2C_MAX])(void* sensor, uint8_t reg, uint8_t val);

	//sensors - message processors
	//tablica wskaznikow do funkcji
	void (*sensor_message_processors_fun[vSENSOR_MAX])(void *, char*);
	void* sensors_object_types[vSENSOR_MAX];

	//function that forwards messages to emulator
	void (*fun_forwarder)(char*);
} vSensorManager_t;

void vSensorManager_init(vSensorManager_t* vSensorManager);
void vSensorManager_ProcessMessage(vSensorManager_t* vSensorManager, char* message);
void vSensorManager_set_forwarder(vSensorManager_t* vSensorManager, void (*fun_forwarder)(char*));

//i2c messages
uint8_t vSensorManager_i2c_readRegister(vSensorManager_t* vSensorManager, uint16_t address, uint8_t reg);
uint8_t* vSensorManager_i2c_readRegisters(vSensorManager_t* vSensorManager, uint16_t address, uint8_t reg);
uint8_t vSensorManager_i2c_readRegisterSize(vSensorManager_t* vSensorManager, uint16_t address, uint8_t reg);
void vSensorManager_i2c_writeRegister(vSensorManager_t* vSensorManager, uint16_t address, uint8_t reg, uint8_t val);

#ifdef __cplusplus
} // extern "C"
#endif

#endif /* VSENSORMANAGER_H_ */
