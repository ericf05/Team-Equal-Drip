import RPi.GPIO as GPIO
import spidev
import signal
import sys
import time

GPIO.setmode(GPIO.BOARD)

spi_ch = 0
spi = spidev.SpiDev(0, spi_ch)
spi.max_speed_hz = 1200000

GPIO.setwarnings(False)

GPIO.setup(15, GPIO.OUT)
# GPIO.setup(16, GPIO.OUT)



def close(signal, frame):
    GPIO.output(15, 0)
   #GPIO.output(16, 0)

signal.signal(signal.SIGINT, close)

def valmap(value, istart, istop, ostart, ostop):
    value = ostart + (ostop - ostart) * ((value - istart) / (istop - istart))
    if value > ostop:
        value = ostop
    return value

def get_adc(channel):
    if channel != 0:
        channel = 1
        
    msg = 0b11
    msg = ((msg << 1) + channel) << 5
    msg = [msg, 0b00000000]
    reply = spi.xfer2(msg)
    
    adc = 0
    for n in reply:
        adc = (adc << 8) + n
        
    adc = adc >> 1
    voltage = (5 * adc) / 1024
    
    return voltage
    
def compute_moisture_percentage(sensor_reading):
    # Known values
    x1 = 2.64  # Sensor reading for completely dry soil
    y1 = 0     # Corresponding moisture percentage for x1
    x2 = 1.82  # Sensor reading for just watered soil
    y2 = 100   # Corresponding moisture percentage for x2

    # Calculate slope (m)
    m = (y2 - y1) / (x2 - x1)

    # Calculate intercept (b)
    b = y1 - m * x1

    # Compute moisture percentage (y)
    moisture_percentage = m * sensor_reading + b

    return moisture_percentage

def main():
    try:
        adc_0 = get_adc(0)
        adc_1 = get_adc(1)
        # print(adc_0, adc_1)
        sensor1 = round(adc_0, 2)
        if sensor1 < 0.5:
            moisture = 0
        else: 
            moisture = round(valmap(sensor1, 5, 3.5, 0, 100), 0)
        sensor2 = round(adc_1, 2)
        #if sensor2 < 0.5:
         #   moisture2 = 0
        #else: 
           # moisture2 = round(valmap(sensor2, 5, 3.5, 0, 100), 0)
        
        if moisture < 40:
            GPIO.output(15, 1)
           # GPIO.output(16, 0)
        else:
            GPIO.output(15, 0)
            #GPIO.output(16, 1)
        time.sleep(2)
	
    except Exception as error:
        print('ERROR: ' + str(error))
        sensor1 = 0 

    reading = compute_moisture_percentage(sensor1)
    #print(compute_moisture_percentage(sensor1), moisture)
    return (sensor1, reading)

if __name__ == "__main__":
	print(main())
	GPIO.cleanup()
