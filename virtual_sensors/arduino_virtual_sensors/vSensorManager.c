#include <stdlib.h>
#include <stdio.h>
#include "vSensorManager.h"
#include "vGPIOS.h"
#include "vBME280.h"


////////////////////////////////////////////////////////
// Message Dispatcher //
////////////////////////////////////////////////////////
void vSensorManager_ProcessMessage(vSensorManager_t* vSensorManager, char* message) {

//C|543|BME280|PD0;PD1
//C|453|BME280|wiring
//R

//C|35|GPIO|SENSOR|PD0
//C|35|GPIO|ACTUATOR|PD1

//V

//F|543|settings
//F|543|values

//B|543|results

	char sensor_name[20];
	int sensor_number;
	int message_offset = 2;

	//remove new lines characters
	vSensor_strfinaltrim(message);

	if (message[0] == 'C') {
		//read sensor id
		message_offset += vSensor_parse_int(message + message_offset,
				&sensor_number);

		message_offset++;

		//read sensor name
		message_offset += vSensor_conditional_strcpy(message + message_offset,
				sensor_name, '|');

		message_offset++;

		//if sensor_name equals GPIOS
		if (!vSensor_conditional_strcmp("GPIOS", sensor_name)) {
			vGPIOS_t* gpios_sens_p;
			gpios_sens_p = (vGPIOS_t*)malloc(sizeof(vGPIOS_t));
			vGPIOS_config(vSensorManager, sensor_number, gpios_sens_p, message + message_offset);
		} else if (!vSensor_conditional_strcmp("BME280", sensor_name)) {
			vBME280_t vbme280_sens;
			//vSensorManager->sensors_object_types[sensor_number] = &vbme280_sens;
			//vSensorManager->sensor_message_processors_fun[sensor_number] = &vBME280_config;
			//vBME280_config(vSensorManager, &vbme280_sens, message+message_offset);
		}
	} else if (message[0] == 'R') {
		//TODO
	} else if (message[0] == 'F') {
		//read sensor id
		message_offset += vSensor_parse_int(message + message_offset, &sensor_number);
		message_offset++;
		(*vSensorManager->sensor_message_processors_fun[sensor_number])(vSensorManager->sensors_object_types[sensor_number], message + message_offset);
	} else if (message[0] == 'V') {
		//send version back
		(*vSensorManager->fun_forwarder)(vSENSOR_VERSION);
	}
}
//(*fun_ptr)(10);
void vSensorManager_set_forwarder(vSensorManager_t* vSensorManager,
		void (*fun_forwarder)(char*)) {
	vSensorManager->fun_forwarder = fun_forwarder;
}

//ADC dispatcher
//
