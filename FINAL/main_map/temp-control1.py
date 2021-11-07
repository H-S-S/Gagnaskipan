from gpiozero import LED, PWMLED
from signal import pause
from time import sleep
import HTU21D

temp_cont = PWMLED(23)

class tempController():
    def __init__(self, transistor_pin, desired_temp):
        self.tran_pin = transistor_pin
        self.actuator = LED(self.tran_pin)
        self.is_on = True
        self.on_time = 0
        self.off_time = 10
        self.is_constant = False
        self.desired_temp = desired_temp
        #Key: [low sec, high sec]
        self.temp_range = {'0': [10, 0], '1': [9,1],'2': [8, 2],'3': [7, 3],'4': [6, 4],'5': [5, 5],'6': [4, 6],'7': [3, 7],'8': [2, 8],'9': [1, 9],'10': [0, 10] }
        self.current_temp_range = 0
        self.temp_sensor = HTU21D.TempHumidity()
    
    def RUN(self):
        self.controller_max()
        if self.is_on:
            self.one_loop()
        else:
            sleep(10)
        
        self.RUN()

    def one_loop(self):
        self.actuator.on()
        sleep(self.on_time)
        self.actuator.off()
        sleep(self.off_time)



    def turn_off(self):
        self.is_on = False
    def turn_on(self):
        self.is_on = True
        
    def change_temp(self, temp):
        self.on_time, self.off_time = self.calibration_temp(temp)
        
    
    def calibration_temp(self,temp):
        return 10, 10

    def controller(self):
        cur_temp = self.temp_sensor.read_temp()
        temp_diff = cur_temp-self.desired_temp
    
    def controller_max(self):
        cur_temp = self.temp_sensor.read_temp()
        temp_diff = cur_temp-self.desired_temp
        if abs(temp_diff) <= 0.5:
            self.is_on = False
        else:
            self.is_on = True

        self.current_temp_range = 5

        self.on_time = self.temp_range[str(self.current_temp_range)][1]
        self.off_time = self.temp_range[str(self.current_temp_range)][0]

if __name__ == "__main__":
    temp = tempController(23)
    temp.change_temp(10)
    temp.START()


# try:
#     print('ON')
#     temp_cont.value = 0.5
#     sleep(5)
#     print('OFF')
#     temp_cont.value = 0
#     temp_cont.off()
# except KeyboardInterrupt:
#     temp_cont.value = 0
#     temp_cont.off()
#     print("Ctl C pressed - ending program")

# # try:
# #     while True:




# # try:
# #   while True:                      
# #     for dc in range(0, 101, 5):    
# #       pwm.ChangeDutyCycle(dc)
# #       time.sleep(0.05)             
# #       print(dc)
# #     for dc in range(95, 0, -5):    
# #       pwm.ChangeDutyCycle(dc)
# #       time.sleep(0.05)             
# #       print(dc)
# # except KeyboardInterrupt:
# #   print("Ctl C pressed - ending program")
