import rpi_sensor
from emailing import send_email
class Autofarm():
    def __init__(self):
        self.__values = rpi_sensor.read_data()
        self.moisture = self.__values[0]
        self.waterlevel = self.__values[1]
        self.temp = self.__values[2]
        self.humidity = self.__values[3]
    
    def __waterlevel(self):
        if self.waterlevel == 0:
            send_email("Tumiolason@gmail.com")
        
    def __heating(self):
        if self.temp > 0.5: #Raven settu inn rétt gildi hér eða ég skiptir ekki máli
            heater.on()
            return True
        else:
            heater.off()
            return False
        
    def __moisture(self):
        if self.moisture < 0.5: #Eiríkur settu hérna
            watering.on()
            return True
        else:
            watering.off()
            return False
    
    def __monitor(self):
        self.monitor(display(self.__values))

    def main(self):
        while True:
            self.__waterlevel()
            while self.__moisture():
                continue
            self.__heating()
            self.__monitor()
    