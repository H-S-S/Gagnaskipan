import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from time import sleep
from board import SCL, SDA
import busio


def screen_setup():
    i2c = busio.I2C(SCL, SDA)

    # RST = 24
    disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

    disp.begin()

    disp.clear()
    disp.display()

    width = disp.width
    height = disp.height

    image = Image.new('1', (width, height))
    font = ImageFont.load_default()

    padding = -2
    top = padding
    bottom = height-padding
    x = 0
    return image,font,top,x,bottom,disp


def disp_info(temp,humitiy,moist,image,font,top,x,bottom,disp):
    image.text((x, top),'  Temperature: '+str(round(temp,1))+'  ',font=font, fill=255)
    image.text((x, top+8),'    Humidity: '+str(round(humitiy,1))+'   ',font=font, fill=255)
    image.text((x, top+16),'    Moisture: '+str(round(moist,1))+'   ',  font=font, fill=255)
    sleep(.1)