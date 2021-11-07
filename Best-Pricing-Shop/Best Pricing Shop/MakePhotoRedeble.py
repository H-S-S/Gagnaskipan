import cv2
import numpy as np
import matplotlib.pyplot as plt
import pytesseract


#Make adapteble, use histograms and the more of one pixel type the better and clearer the pictures will be

class makePhotoRedeble():

    def __init__(self, img):
        self.image = self.resize_img(img, 0.75, 0.4)
        gray = cv2.cvtColor(self.image.copy(), cv2.COLOR_BGR2GRAY)
        adapt_thres = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 8)

        self.final_image = adapt_thres

    def resize_img(self, img, rezise_x=0.75, rezise_y=0.75):
        width = int(img.shape[1] * rezise_x)
        height = int(img.shape[0] * rezise_y)
        #print(height, width)

        dimentions = (width, height)
        return cv2.resize(img, dimentions, interpolation=cv2.INTER_AREA)

    def return_rezise_image(self):
        return self.image
    def return_final_image(self):
        return self.final_image