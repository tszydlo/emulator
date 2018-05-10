//#include "vSensorManager.h"
#include "vBME280.h"

void vBME280_init(vBME280_t* sensor){
	for(int i=0; i<94; i++){
		sensor->memory[i] = 0;
	}

	sensor->memory[0xD0-(0x88)]=0x60;

	//dig_T1
	sensor->memory[(0x88)-(0x88)]=27504 & 0xFF;
	sensor->memory[0x89-(0x88)]=27504 >> 8;

	//dig_T2
	sensor->memory[0x8A-(0x88)]=26435 & 0xFF;
	sensor->memory[0x8B-(0x88)]=26435 >> 8;

	//dig_T3
	sensor->memory[0x8C-(0x88)]=0x00;
	sensor->memory[0x8D-(0x88)]=0x00;

	//double dig_P1 = 36477;
	sensor->memory[(0x8E)-(0x88)]=36477 & 0xFF;
	sensor->memory[(0x8F)-(0x88)]=36477 >> 8;

	//double dig_P2 = 0;
	sensor->memory[0x90-(0x88)]=0 & 0xFF;
	sensor->memory[0x91-(0x88)]=0 >> 8;

	//double dig_P3 = 0;
	sensor->memory[0x92-(0x88)]=0 & 0xFF;
	sensor->memory[0x93-(0x88)]=0 >> 8;

	//double dig_P4 = 2855;
	sensor->memory[0x94-(0x88)]=2855 & 0xFF;
	sensor->memory[0x95-(0x88)]=2855 >> 8;

	//double dig_P5 = 0;
	sensor->memory[0x96-(0x88)]=0 & 0xFF;
	sensor->memory[0x97-(0x88)]=0 >> 8;

	//double dig_P6 = 0;
	sensor->memory[0x98-(0x88)]=0 & 0xFF;
	sensor->memory[0x99-(0x88)]=0 >> 8;

	//double dig_P7 = 15500;
	sensor->memory[0x9A-(0x88)]=15500 & 0xFF;
	sensor->memory[0x9B-(0x88)]=15500 >> 8;

	//double dig_P8 = -14600;
	sensor->memory[0x9C-(0x88)]=-14600 & 0xFF;
	sensor->memory[0x9D-(0x88)]=-14600 >> 8;

	//double dig_P9 = 0;
	sensor->memory[(0x9E)-(0x88)]=0 & 0xFF;
	sensor->memory[(0x9F)-(0x88)]=0 >> 8;

	//double dig_H1 = 0;
	sensor->memory[0xA1-(0x88)]=0;

	//double dig_H2 = 368;
	sensor->memory[0xE1-(0x88)]=368 & 0xFF;
	sensor->memory[0xE2-(0x88)]=368 >> 8;

	//double dig_H3 = 0;
	sensor->memory[0xE3-(0x88)]=0;

	//double dig_H4 = 0; dig_H5 = 0;
	sensor->memory[0xE4-(0x88)]=0;
	sensor->memory[0xE5-(0x88)]=0;
	sensor->memory[0xE6-(0x88)]=0;

	//double dig_H6 = 0;

	sensor->memory[0xE7-(0x88)]=0;
}

void vBME280_config(vSensorManager_t* sensor_manager, int sensor_id, vBME280_t* sensor, char* command){
	vBME280_init(sensor);

	uint8_t sensor_number = sensor_manager->i2c_vsensors_count;

	sensor_manager->i2c_vsensors_addresses[ sensor_number ] = vBME280_addr;
	sensor_manager->i2c_vsensors_count++;

	sensor_manager->i2c_readRegisterSize_fun[sensor_number] = &vBME280_readRegisterSize;
	sensor_manager->i2c_readRegister_fun[sensor_number] = &vBME280_readRegister;
	sensor_manager->i2c_readRegisters_fun[sensor_number] = &vBME280_readRegisters;
	sensor_manager->i2c_writeRegister_fun[sensor_number] = &vBME280_writeRegister;

	sensor_manager->sensors_object_types[sensor_id] = sensor;
	sensor_manager->i2c_vsensors_id[sensor_number] = sensor_id;
	sensor_manager->sensor_message_processors_fun[sensor_id] = &vBME280_ProcessMessage;

	vSensorManager_setI2C();
	vSensorManager_joinI2C(vBME280_addr);

	//in the current implementation there is nothing to parse in the configuration command
}

//T34.7P948.87H37.0
//void vBME280_config(vSensorManager_t* sensor_manager, int sensor_id, vBME280_t* sensor, char* command){


void vBME280_ProcessMessage(void* sensor_type, char* command){
	char type;
	double value;

	vBME280_t* sensor;
	sensor = (vBME280_t*)sensor_type;

	int idx=0;
	int res_idx;

	while (command[idx]){
		type = command[idx];
		idx++;
		res_idx = vSensor_parse_double(command+idx, &value);

		if (res_idx==-1) return;

		idx+=res_idx;

		printf("Type=%c value=%f\n", type, value);

		if (type == 'T') vBME280_setTemp(sensor, value);
		else if (type == 'P') vBME280_setPressure(sensor, value);
		else if (type == 'H') vBME280_setHumidity(sensor, value);
	}
}

void vBME280_setTemp(vBME280_t* sensor, double t){
	uint32_t adc_t;

	adc_t = -((-0.8388608e8)*(727068240/0.524288e7+t))/26435;

	sensor->temp = t;

	//20 bit value
	sensor->memory[0xFA-(0x88)]=(adc_t>>12) & 0xFF;
	sensor->memory[0xFB-(0x88)]=(adc_t>>4) & 0xFF;
	sensor->memory[0xFC-(0x88)]=adc_t & 0x0F<<4;
}

void vBME280_setHumidity(vBME280_t* sensor, double h){
	uint32_t adc_hum;

	adc_hum = 178 * h;

	sensor->memory[0xFD-(0x88)]=(adc_hum>>8) & 0xFF;
	sensor->memory[(0xFE)-((0x88))]=(adc_hum & 0xFF);
}

void vBME280_setPressure(vBME280_t* sensor, double p){
	uint32_t adc_press;

	adc_press = - 6.0035012429 * (p-0.1680206019e6);

	sensor->memory[0xF7-(0x88)]=(adc_press>>12) & 0xFF;
	sensor->memory[0xF8-(0x88)]=(adc_press>>4) & 0xFF;
	sensor->memory[0xF9-(0x88)]=adc_press&0x0F<<4;
}

uint8_t vBME280_readRegister(void* sensor_type, uint8_t reg){
	vBME280_t* sensor;
	sensor = (vBME280_t*)sensor_type;

	return sensor->memory[reg-(0x88)];
}

uint8_t* vBME280_readRegisters(void* sensor_type, uint8_t reg){
	vBME280_t* sensor;
	sensor = (vBME280_t*)sensor_type;

	return &(sensor->memory[reg-(0x88)]);
}
uint8_t vBME280_readRegisterSize(void* sensor_type, uint8_t reg){
	vBME280_t* sensor;
	sensor = (vBME280_t*)sensor_type;

	if ((reg==0xD0) || (reg==0xF2) || (reg==0xF3) || (reg==0xF4) || (reg==0xF5) || (reg==0xA1) || (reg==0xA3)){
		return 1;
	} else if ((reg==0xF7) || (reg==0xFA)){
		return 3;
	} else return 2;
}

void vBME280_writeRegister(void* sensor_type, uint8_t reg, uint8_t val){
	vBME280_t* sensor;
	sensor = (vBME280_t*)sensor_type;

	return;
}

////////////////////////////////////////////////////////////////////
// TESTING //
/*
double dig_T1 = 27504;
double dig_T2 = 26435;
double dig_T3 = 0;

int32_t t_fine;

double vBME280_compensate_T_double(int32_t adc_T){
	double var1, var2, T;
	var1  = (((double)adc_T)/16384.0 - ((double)dig_T1)/1024.0) * ((double)dig_T2);
	var2  = ((((double)adc_T)/131072.0-((double)dig_T1)/8192.0) *(((double)adc_T)/131072.0-((double)dig_T1)/8192.0)) * ((double)dig_T3);
	t_fine = (int32_t)(var1 + var2);
	T  = (var1 + var2) / 5120.0;
	return T;
}

double dig_P1 = 36477;
double dig_P2 = 0;
double dig_P3 = 0;
double dig_P4 = 2855;
double dig_P5 = 0;
double dig_P6 = 0;
double dig_P7 = 15500;
double dig_P8 = -14600;
double dig_P9 = 0;

// Returns pressure in Pa as double. Output value of 96386.2 equals 96386.2 Pa = 963.862 hPa
double vBME280_compensate_P_double(int32_t adc_P){
	double var1, var2, p;
	var1 = ((double)t_fine/2.0)-64000.0;
	var2 = var1 * var1 * ((double)dig_P6) / 32768.0;
	var2 = var2 + var1 * ((double)dig_P5) * 2.0;
	var2 = (var2/4.0)+(((double)dig_P4) * 65536.0);
	var1 = (((double)dig_P3) * var1 * var1 / 524288.0 + ((double)dig_P2) * var1) / 524288.0;
	var1 = (1.0 + var1 / 32768.0)*((double)dig_P1);
	if (var1 == 0.0)
	{
		return 0;
		// avoid exception caused by division by zero
	}
	p = 1048576.0-((double)adc_P);
	p = (p-(var2 / 4096.0)) * 6250.0 / var1;
	var1 = ((double)dig_P9) * p * p / 2147483648.0;
	var2 = p * ((double)dig_P8) / 32768.0;
	p = p + (var1 + var2 + ((double)dig_P7)) / 16.0;
	return p;
}

double dig_H1 = 0;
double dig_H2 = 368;
double dig_H3 = 0;
double dig_H4 = 0;
double dig_H5 = 0;
double dig_H6 = 0;


// Returns humidity in % rH as as double. Output value of 46.332 represents 46.332 % rH
double vBME280_compensate_H_double(int32_t adc_H){
	double var_H;
	var_H = (((double)t_fine)-76800.0);
	var_H = (adc_H-(((double)dig_H4)*64.0+((double)dig_H5) / 16384.0 * var_H))*(((double)dig_H2)/65536.0*(1.0 +((double)dig_H6)/67108864.0*var_H*(1.0+((double)dig_H3)/67108864.0*var_H)));
	var_H = var_H * (1.0-((double)dig_H1)*var_H/524288.0);
	if (var_H > 100.0) var_H = 100.0;
	else if (var_H < 0.0) var_H = 0.0;
	return var_H;
}
*/
