/*
 * vGPIOS.c
 *
 *  Created on: 29.03.2018
 *      Author: User
 */

#include "vGPIOS.h"

// GPIOS - sensor that uses GPIO
// GPIO as output in emulator

void vGPIOS_config(vSensorManager_t* sensor_manager, int sensor_id, vGPIOS_t* sensor, char* command){
	//printf("[GPIOS]%s\n",command);

	//set the sensor_manager structure
	sensor_manager->sensors_object_types[sensor_id] = sensor;
	sensor_manager->sensor_message_processors_fun[sensor_id] = &vGPIOS_ProcessMessage;
	vSensor_conditional_strcpy(command, sensor->port,0);

	//set output
	vSensorManager_setPinDirection(command, vSENSOR_GPIO_OUTPUT);
}


void vGPIOS_ProcessMessage(void* sensor_type, char* command){
	//printf("[GPIOS - F]%s\n",command);

	vGPIOS_t* pointer;
	pointer = (vGPIOS_t*)sensor_type;

	if (command[0]=='0'){
		vSensorManager_setPinState(pointer->port, vSENSOR_GPIO_OFF);
	} else {
		vSensorManager_setPinState(pointer->port, vSENSOR_GPIO_ON);
	}
}
