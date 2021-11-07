import time
import board
import busio
from adafruit_htu21d import HTU21D

i2c = busio.I2C(board.SCL, board.SDA)

class TempHumidity():
    def __init__(self):
        self.sensor = HTU21D(i2c)

    def read_temp(self):
        return self.sensor.temperature

    def read_humidity(self):
        return self.sensor.relative_humidity

if __name__ == "__main__":
    t = TempHumidity()
    while True:
        print("\nTemperature: %0.1f C" % t.read_temp())
        print("Humidity: %0.1f %%" % t.read_humidity())
        time.sleep(1)
