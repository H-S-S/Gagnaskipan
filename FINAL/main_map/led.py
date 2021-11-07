from gpiozero import LED
from io_handler import IO

class LED_control():
    def __init__(self, red_pin, blue_pin, use_feed=False):
        if use_feed:
            self.feed = IO("Mechbois", "aio_GZrL768ax1SSEE2Vl8XWfDdjMZye")
        else:
            self.feed = False

        self.red = LED(red_pin)
        self.blue = LED(blue_pin)

    def red_on(self):
        self.red.on()

    def red_off(self):
        self.red.off()

    def blue_on(self):
        self.blue.on()

    def blue_off(self):
        self.blue.off()

    def purple_on(self):
        self.red_on()
        self.blue_on()
        if self.feed:
            self.feed.send_data('led', 1)

    def purple_off(self):
        self.red_off()
        self.blue_off()
        if self.feed:
            self.feed.send_data('led', 0)

if __name__ == "__main__":
    c = LED_control(26, 19)
    from time import sleep
    while True:
        c.red_on()
        c.blue_off()
        sleep(0.05)
        c.purple_on()
        sleep(0.05)
        c.red_off()
        sleep(0.05)

