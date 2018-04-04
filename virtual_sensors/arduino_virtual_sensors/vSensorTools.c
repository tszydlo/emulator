//TODO add processing of minuses
int vSensor_parse_double(char* str, double *value){
	int idx=0;
	*value = 0;
	int fp = 0;
	double div=0;

	while(str[idx] != 0){

		if ((str[idx]>='0')&&(str[idx]<='9') && !fp){
			*value = *value * 10 + (str[idx]-'0');
		} else if ((str[idx]>='0')&&(str[idx]<='9') && fp){
			div=div*10.0;
			*value = *value + 1.0*(str[idx]-'0')/div;
		} else if (str[idx]=='.') {
			fp=1;
			div=1.0;
		} else return idx;
		idx++;
	}

	return idx;
}

//TODO add processing of minuses
int vSensor_parse_int(char* str, int *value){
	int idx=0;
	*value = 0;

	while(str[idx] != 0){

		if ((str[idx]>='0')&&(str[idx]<='9')){
			*value = *value * 10 + (str[idx]-'0');
		} else return idx;
		idx++;
	}
	return idx;
}


int vSensor_conditional_strcpy(char* src, char* dst, char marker){
	int index=0;

	while (src[index]!= 0 && src[index]!=marker){
		dst[index]=src[index];
		index++;
	}
	dst[index]=0;
	return index;
}

int vSensor_conditional_strcmp(char* str1, char* str2){
	int idx=0;

	do {
		if (str1[idx]!=str2[idx]) return -1;
		idx++;
	} while (str1[idx]!=0 && str2[idx]!=0);

	return 0;
}

void vSensor_strfinaltrim(char* str){
	int idx=0;

	while (str[idx]!= 0){
		if (str[idx]==0x0A || str[idx]==0x80) {
			str[idx]=0;
			return;
		}
		idx++;
	}
}

