from adc import ADC
from HTU21D import TempHumidity
from water_level import WaterLevel
from io_handler import IO
from led import LED_control
from time import sleep

# Constants
SLEEP_TIME = 5

# Pins
red = 26
blue = 19
moisture_pin_adc = 0 # Pin in the ADC
moisture_pin = 27
water_level_pin = 5

# Setup
moist_obj = ADC(moisture_pin)
temp_obj = TempHumidity()
water_obj = WaterLevel(water_level_pin)
feed = IO("Mechbois", "aio_GZrL768ax1SSEE2Vl8XWfDdjMZye")
led = LED_control(red_pin=red, blue_pin=blue)

def run(print_cmd=False):
    # Get sensor value and send data
    moist_val, water_val, temp_val, humid_val = sensor_handler(print_cmd)

    # TODO Handle the data

    # # Temporary
    # if water_val == 0:
    #     send_email("tumi19@ru.is")

    if moist_val > 50:
        led.purple_on()
    else:
        led.purple_off()

    sleep(SLEEP_TIME)

def read_data():
    '''Reads in data from 4 sensors, returns values as list.'''
    moist_val = moist_obj.read(moisture_pin_adc)    # Read moisture
    water_val = water_obj.read()                    # Read water level
    temp_val = temp_obj.read_temp()                 # Read Temperature
    humid_val = temp_obj.read_humidity()            # Read humidity
    return [moist_val, water_val, temp_val, humid_val]

def sensor_handler(print_cmd=False):
    '''Reads, sends and prints out data.'''
    # read data
    moist_val, water_val, temp_val, humid_val = read_data()

    #send data
    feed.send_data('moisture', moist_val)
    feed.send_data('water-level', water_val)
    feed.send_data('temperature', temp_val)
    feed.send_data('humidity', humid_val)

    # print to terminal if specified
    if print_cmd:
        lis = [('Moisture', moist_val), ('Water Level', water_val), ('Temperature', temp_val), ('Humidity', humid_val)]
        print_data(lis)
        
    return moist_val, water_val, temp_val, humid_val

def print_data(lis):
    '''Prints data to terminal'''
    for string, data in lis:
        print(f'{string}: {round(data,3)}')

if __name__ == "__main__":
    while True:
        run(print_cmd=True)
