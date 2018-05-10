/*
 * vGPIO.h
 *
 *  Created on: 24.03.2018
 *      Author: User
 */
#ifndef VGPIOA_H_
#define VGPIOA_H_

#include <stdint.h>
#include "vSensorManager.h"

typedef struct {
	uint8_t memory[118];
	//0-IN, 1-OUT
	int direction;
	int state;
} vGPIO_t;


void vGPIO_config(vSensorManager_t* sensor_manager, vGPIO_t* sensor, char* command);
void vGPIO_ProcessMessage(void* sensor_type, char* command);

#endif /* VGPIOA_H_ */
