FROM tszydlo/docker-fogdevices
RUN apk add py-setuptools
RUN easy_install-2.7 requests
RUN   apk update && apk add ca-certificates wget && update-ca-certificates
RUN export MRAA_FOGDEVICES_PLATFORM_ID="$DEVICE_ID"
RUN export MRAA_FOGDEVICES_PLATFORM_BROKER="iot.eclipse.org"
RUN cd /root
RUN wget https://github.com/tszydlo/device_app/blob/master/artik_lm35.py 
CMD python artik_lm35.py $ARTIK_DEVICE_ID $ARTIK_TOKEN 
