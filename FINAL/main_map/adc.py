import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from gpiozero import LED
from time import sleep
i2c = busio.I2C(board.SCL, board.SDA)

class ADC:
    '''
    Made for ADC board ADS1115
    Connect the board up, then function
    read returns data corresponding to chosen pin
    '''
    def __init__(self, pin):
        self.gpio_pin = LED(pin)

        # I2C sensor object to send to
        self.sensor = ADS.ADS1115(i2c)

        # ADC module requires pins as objects, this maps it out
        # for easier use, simply input an integer from 0 to 3.
        self.pinmap = {0:ADS.P0, 1:ADS.P1, 2:ADS.P2, 3:ADS.P3}

    def read(self, pin):
        '''Returns analog data corresponging to pin'''
        self.gpio_pin.on()
        sleep(0.05)
        ret_val = AnalogIn(self.sensor, self.pinmap[pin]).value * (100/21632)
        self.gpio_pin.off()
        return ret_val


if __name__ == "__main__":
    moist_obj = ADC(27)
    while True:
        print(moist_obj.read(0))
        sleep(0.5)        


    # while True:
    #     pot = analogread(ads, ADS.P0)
    #     moist = analogread(ads, ADS.P1)
    #     print('Potentiometer: ', pot.value)
    #     print('Moisture: ', moist.value)
    #     sleep(0.5)

