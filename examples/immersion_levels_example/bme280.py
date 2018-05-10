from __future__ import print_function
import time, sys, signal, atexit
from upm import pyupm_bmp280 as sensorObj

def main():
    # Instantiate a BME280 instance using default i2c bus and address
    sensor = sensorObj.BME280()

    ## Exit handlers ##
    # This function stops python from printing a stacktrace when you hit control-C
    def SIGINTHandler(signum, frame):
        raise SystemExit

    # This function lets you run code on exit
    def exitHandler():
        print("Exiting")
        sys.exit(0)

    # Register exit handlers
    atexit.register(exitHandler)
    signal.signal(signal.SIGINT, SIGINTHandler)

    while (1):
        sensor.update()

        print("Compensation Temperature:", sensor.getTemperature(), "C /", end=' ')
        print(sensor.getTemperature(True), "F")

        print("Pressure: ", sensor.getPressure(), "Pa")

        print("Computed Altitude:", sensor.getAltitude(), "m")

        print("Humidity:", sensor.getHumidity(), "%RH")

        print()
        time.sleep(1)

if __name__ == '__main__':
    main()