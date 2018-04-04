/*
 * vSensorTools.h
 *
 *  Created on: 24.03.2018
 *      Author: User
 */

#ifndef VSENSORTOOLS_H_
#define VSENSORTOOLS_H_

#ifdef __cplusplus
extern "C" {
#endif

int vSensor_parse_double(char* str, double *value);
int vSensor_parse_int(char* str, int *value);
int vSensor_conditional_strcpy(char* src, char* dst, char marker);
int vSensor_conditional_strcmp(char* str1, char* str2);
void vSensor_strfinaltrim(char* str);

#ifdef __cplusplus
} // extern "C"
#endif

#endif /* VSENSORTOOLS_H_ */
