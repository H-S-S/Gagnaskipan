import cv2
import numpy as np
import matplotlib.pyplot as plt
import pytesseract
import MakePhotoRedeble as MPR

pytesseract.pytesseract.tesseract_cmd = "D:\\Program\\Tesseract\\tesseract.exe"
GREEN = (0, 255, 0)






img_path_1 = "Photos/photo5.jpg"
img_path_2 = "Photos/photo6.jpg"

img_1 = cv2.imread(img_path_1)
img_2 = cv2.imread(img_path_2)



adaptive_1 = MPR.makePhotoRedeble(img_1).return_final_image()
adaptive_2 = MPR.makePhotoRedeble(img_2).return_final_image()

blank = np.zeros(adaptive_1.shape, dtype = "uint8")

cont, hierarcies = cv2.findContours(adaptive_1, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

img_1_draw = MPR.makePhotoRedeble(img_1).return_rezise_image()
cv2.drawContours(img_1_draw, cont[1], -1, (0, 0, 255), 1)
print(cont[1][1])

#cv2.imshow("Ad 1", adaptive_1)
#cv2.imshow("Ad 2", adaptive_2)

#cv2.imshow("Cont", img_1_draw)
#plt.plot(cont[1][0])

#plt.show()
cv2.waitKey(0)
cv2.destroyAllWindows()

