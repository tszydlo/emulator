/*
 * vGPIOS.h
 *
 *  Created on: 29.03.2018
 *      Author: User
 */

#ifndef VGPIOS_H_
#define VGPIOS_H_

#include "vSensorManager.h"

typedef struct {
	//we do not want to use malloc
	char port[6];
	int state;
} vGPIOS_t;

void vGPIOS_config(vSensorManager_t* sensor_manager, int sensor_id, vGPIOS_t* sensor, char* command);
void vGPIOS_ProcessMessage(void* sensor_type, char* command);


#endif /* VGPIOS_H_ */
