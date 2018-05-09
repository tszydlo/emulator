/*
 * vBME280.h
 *
 *  Created on: 08.03.2018
 *      Author: User
 */

#ifndef VBME280_H_
#define VBME280_H_

#include "vSensorManager.h"

#define vBME280_addr 0x77

typedef struct {
	uint8_t memory[118];

	double temp;
	double hum;
	double press;
} vBME280_t;

#ifdef __cplusplus
extern "C" {
#endif

//void vBME280_init(vBME280_t* sensor);

void vBME280_setTemp(vBME280_t* sensor, double t);
void vBME280_setHumidity(vBME280_t* sensor, double h);
void vBME280_setPressure(vBME280_t* sensor, double p);

//uint8_t vBME280_readRegister(vBME280_t* sensor, uint8_t reg);
//uint8_t* vBME280_readRegisters(vBME280_t* sensor, uint8_t reg);
//uint8_t vBME280_readRegisterSize(vBME280_t* sensor, uint8_t reg);
//void vBME280_writeRegister(vBME280_t* sensor, uint8_t reg, uint8_t val);

//uint8_t (*i2c_readRegister_fun[vSENSOR_I2C_MAX])(void* sensor, uint8_t reg);
//uint8_t* (*i2c_readRegisters_fun[vSENSOR_I2C_MAX])(void* sensor, uint8_t reg);
//uint8_t (*i2c_readRegisterSize_fun[vSENSOR_I2C_MAX])(void* sensor, uint8_t reg);
//void (*i2c_writeRegister_fun[vSENSOR_I2C_MAX])(void* sensor, uint8_t reg, uint8_t val);

uint8_t vBME280_readRegister(void* sensor_type, uint8_t reg);
uint8_t* vBME280_readRegisters(void* sensor_type, uint8_t reg);
uint8_t vBME280_readRegisterSize(void* sensor_type, uint8_t reg);
void vBME280_writeRegister(void* sensor_type, uint8_t reg, uint8_t val);

void vBME280_config(vSensorManager_t* sensor_manager, int sensor_id, vBME280_t* sensor, char* command);
void vBME280_ProcessMessage(void* sensor_type, char* command);
void vBME280_init(vBME280_t* sensor);

//TEST
//double vBME280_compensate_T_double(int32_t adc_T);
//double vBME280_compensate_P_double(int32_t adc_P);
//double vBME280_compensate_H_double(int32_t adc_H);


#ifdef __cplusplus
} // extern "C"
#endif

#endif /* VBME280_H_ */
