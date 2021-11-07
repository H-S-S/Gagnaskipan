from random import randint
from Adafruit_IO import Client, Feed
from time import sleep

class IO():
    def __init__(self, username, key):
        self.client = Client(username, key)

    def receive_data(self, feed_key):
        return self.client.receive(feed_key)

    def send_data(self, feed_key, data):
        return self.client.send(feed_key, data)

if __name__ == "__main__":
    ADAFRUIT_IO_USERNAME = "Mechbois"
    ADAFRUIT_IO_KEY = "aio_GZrL768ax1SSEE2Vl8XWfDdjMZye"  
    aio = IO(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
    
    def get_new_number(num, inc):
        inc = randint(-inc, inc)
        num += inc

        num = 0 if num < 0 else num
        num = 1023 if num > 1023 else num

        return num

    num = int(1023/2)
    while True:
        num = get_new_number(num, 15)
        print('Sending:', num)
        aio.send_data('info', num)

        trigger = aio.receive_data('trigger')
        print('Trigger is:', trigger.value)

        print()
        sleep(3)