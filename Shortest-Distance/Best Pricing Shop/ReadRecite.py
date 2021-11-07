import cv2
import numpy as np
import matplotlib.pyplot as plt
import pytesseract

pytesseract.pytesseract.tesseract_cmd = "D:\\Program\\Tesseract\\tesseract.exe"
GREEN = (0, 255, 0)

#The precition of the lines, the minimum distance between points
PRESITION_Y = 20
#PRESITION_X = 75
PRESITION_X = 75
LINE_LENGTH_REQURIMENT = 25

#To do not in order
#add together the right side numbers and if it did not equal the total on the bottom something went wrong
#split the resict into to parts the cost and the item.
#Use edge detection to only find the resipt or make user crop it.



class Loads_img():
    def __init__(self, path):
        self.path = path
        self.img = cv2.imread(self.path)

    def returns_img(self):
        return self.img



class Makes_Img_Redeble():
    def __init__(self, img):
        self.img = img
        self.img_height = img.shape[0]
        #img_resize = cv2.resize(img, None, fx = 0.5, fy = 0.5)
        img_gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        #self.img_adaptive = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY, 99, 25)
        self.img_adaptive = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15,8)
        self.img_final = self.img_adaptive

    def returns_img(self):
        return self.img_final

class Find_Lines():
    def __init__(self, img):
        self.img = img
        self.img_height = img.shape[0]
        self.original_img = img
        self.shape = self.img.shape
        self.img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        self.ret, self.thres = cv2.threshold(self.img_gray, 127, 255, 0)


        min_max_shapes = self.min_max_shape()

        #makes average from min and max x and y so only one vector for each pont
        self.the_points_positions = self.average_from_min_max_vector(min_max_shapes)

        #sorts the array of tuple by x value then y value so y value desides.
        self.the_points_positions.sort(key = lambda x:x[0])
        self.the_points_positions.sort(key= lambda x:x[1])

        #makes an array of arrays that are in a range so if the picture is 100 high then it makes 100/precition_y for
        #example 100/20 = 5 arrays with the range -20:20 0:40 20:60 40:60 60:80 80:100
        arrays_of_array_of_the_points_positions = self.sorts_points_in_array_depending_on_y(self.the_points_positions)



        # make lines if the dots are close enogh
        #makes lines with matching y values with an error of +-PRESITION
        #constants
        self.the_line_array = self.makes_lines_if_close_enogh(self.the_points_positions)

        self.the_line_array2 = self.makes_lines_if_close_enogh_2(arrays_of_array_of_the_points_positions)
        print(self.the_line_array2)
        #print("Length line array:", len(the_line_array))
        #self.the_line_array.sort(key=lambda x: x[0])
        #self.the_line_array.sort(key=lambda x: x[1])



        #combines lines if they are close together

        #self.combines_lines_array = self.combine_lines(the_line_array)
        self.combines_lines_array = self.combine_lines(self.the_line_array2)

        #Takes out lines that are shorter than REQURED LINE LENGTH
        REQUIRED_LINE_LENGHT = 400
        self.final_line_array = []
        for i in range(len(self.combines_lines_array)):
            x_length = self.combines_lines_array[i][1][0] - self.combines_lines_array[i][0][0]
            if abs(x_length) >= REQUIRED_LINE_LENGHT:
                self.final_line_array.append(self.combines_lines_array[i])

        #print("Length final line array:", len(self.final_line_array))


        #print(combined_lines_array[29])

    def returns_devided_images(self):
        #devides the images based on the lines so for every line there will be a new image
        MIN_WINDOW_REQ = 75
        all_images = []
        start_y = 0

        for i in range(len(self.final_line_array)):
            min_y = self.final_line_array[i][0][1]
            #print("Stars: {} Ends: {}".format(start_y, min_y))
            if abs(min_y - start_y) >= MIN_WINDOW_REQ:
                img= self.img[start_y:min_y, 0:]
                cv2.imshow("test", img)
                all_images.append(img)
            start_y = min_y

            if (i+1) == len(self.final_line_array):
                if abs(start_y - min_y) >= MIN_WINDOW_REQ:
                    all_images.append(self.img[start_y:, 0: ])


        return all_images

    def sorts_points_in_array_depending_on_y(self, the_points_positions):
        amount_of_arrays = int(round(self.img_height/PRESITION_Y, 0))
        the_points_position_array_of_array = []
        for i in range(amount_of_arrays):
            the_points_position_array_of_array.append([])
        for i in range(len(the_points_positions)):
            for ii in range(amount_of_arrays):
                y_value = the_points_positions[i][1]
                y_value_min = y_value - PRESITION_Y
                y_value_max = y_value + PRESITION_Y

                if (y_value_min) >= ((ii-1)*PRESITION_Y) and (y_value_min) <= ((ii+1)*PRESITION_Y):
                    the_points_position_array_of_array[ii].append(the_points_positions[i])


                elif (y_value_max) >= ((ii-1)*PRESITION_Y) and (y_value_max) <= ((ii+1)*PRESITION_Y):
                    the_points_position_array_of_array[ii].append(the_points_positions[i])

        return the_points_position_array_of_array

    def makes_lines_if_close_enogh_2(self, array_of_array_points):
        the_line_array = []
        #sorts all arrays by x value
        for array in array_of_array_points:
            array.sort(key=lambda x: x[0], reverse=False)

        for i in range(len(array_of_array_points)):
            min_x = array_of_array_points[i][0][0]
            max_x = array_of_array_points[i][0][0]
            min_y = array_of_array_points[i][0][1]
            max_y = array_of_array_points[i][0][1]

            first_x = array_of_array_points[i][0][0]
            first_y = array_of_array_points[i][0][1]
            for ii in range(len(array_of_array_points[i])):

                x_value = array_of_array_points[i][ii][0]
                y_value = array_of_array_points[i][ii][1]

                if abs(x_value-max_x) <= PRESITION_X:
                    if x_value > max_x:
                        max_x = x_value
                    if x_value < min_x:
                        min_x = x_value
                    if y_value > max_y:
                        max_y = y_value
                    if y_value < min_y:
                        min_y = y_value
                else:
                    the_line_array.append([(first_x, first_y),(x_value, y_value)])
                    average_y = int(round((min_y+max_y)/2, 0))
                    min_x = array_of_array_points[i][ii][0]
                    max_x = array_of_array_points[i][ii][0]
                    min_y = array_of_array_points[i][ii][1]
                    max_y = array_of_array_points[i][ii][1]

                    first_x = array_of_array_points[i][ii][0]
                    first_y = array_of_array_points[i][ii][1]

                if (ii+1) == len(array_of_array_points[i]):
                    the_line_array.append([(first_x, first_y), (x_value, y_value)])

        return the_line_array




    def min_max_shape(self):
        # Finds and pairs the min x to max x and also min y and min y
        # Makes array and then an aproximite starting and ending possition can be found.
        # if is more a horizontal line the min to max x can be used if vertical y can be used
        cont, hirarchy = cv2.findContours(self.thres, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        min_max_shapes = []
        for i in range(len(cont)):
            # first one is the vector x and y so min_x is the min x and the matching y value for that x and so on
            the_min_x = cont[i][0][0]
            the_min_y = cont[i][0][0]
            the_max_x = cont[i][0][0]
            the_max_y = cont[i][0][0]

            for ii in range(len(cont[i])):
                # if it smaller than current min_x elif if it is larger than the biggest y currently
                # print(cont[i][ii][0][0])
                if cont[i][ii][0][0] < the_min_x[0]:
                    the_min_x = cont[i][ii][0]
                elif cont[i][ii][0][0] > the_max_x[0]:
                    the_max_x = cont[i][ii][0]
                # if it smaller than current min_y elif if it is larger than the biggest y currently
                if cont[i][ii][0][1] < the_min_y[1]:
                    the_min_y = cont[i][ii][0]
                elif cont[i][ii][0][1] > the_max_y[1]:
                    the_max_y = cont[i][ii][0]
                    # print(the_max_y)

            min_max_shapes.append([[(the_min_x[0], the_min_x[1]), (the_max_x[0], the_max_x[1])],
                                   [(the_min_y[0], the_min_y[1]), (the_max_y[0], the_max_y[1])]])
        return min_max_shapes



    def average_from_min_max_vector(self, min_max_shapes):
        the_points_positions = []
        for i in range(len(min_max_shapes)):
            avg_x = int(round((min_max_shapes[i][0][0][0] + min_max_shapes[i][0][1][0]) / 2, 0))
            avg_y = int(round((min_max_shapes[i][1][0][1] + min_max_shapes[i][1][1][1]) / 2, 0))
            the_points_positions.append((avg_x, avg_y))
        return the_points_positions



    def combine_lines(self, the_line_array):
        DISSTANCE_LINE_Y = 20
        DISSTANCE_LINE_X = 30

        combined_lines_array = []
        start_x = the_line_array[0][0][0]
        start_y = the_line_array[0][0][1]
        end_x = the_line_array[0][1][0]
        end_y = the_line_array[0][1][1]

        for i in range(len(the_line_array)):
            start_current_x = the_line_array[i][0][0]
            start_current_y = the_line_array[i][0][1]
            end_current_x = the_line_array[i][1][0]
            end_current_y = the_line_array[i][1][1]
            if abs(start_current_x - end_x) <= DISSTANCE_LINE_X and abs(start_current_y - end_y) <= DISSTANCE_LINE_Y:
                if start_x > start_current_x:
                    start_x = end_current_x
                if end_x < end_current_x:
                    end_x = end_current_x
                if start_y > start_current_y:
                    start_y = start_current_y
                if end_y < end_current_y:
                    end_y = end_current_y
            elif (i + 1) == len(the_line_array):
                combined_lines_array.append([(start_x, start_y), (end_x, end_y)])
            else:
                combined_lines_array.append([(start_x, start_y), (end_x, end_y)])
                start_x = the_line_array[i][0][0]
                start_y = the_line_array[i][0][1]
                end_x = the_line_array[i][1][0]
                end_y = the_line_array[i][1][1]

        return combined_lines_array

    def draw_points(self, points_array, the_img):
        # draws the points from the array
        for i in range(len(points_array)):
            cv2.circle(the_img, points_array[i], radius=1, color=GREEN, thickness=-1)
        return the_img

    def draw_lines(self, final_line_array, the_img):
        # draws the lines
        for i in range(len(final_line_array)):
            cv2.line(the_img, final_line_array[i][0], final_line_array[i][1], GREEN)
        return the_img

    def return_img_lines(self):
        # to return the image

        #self.draw_lines(self.final_line_array, self.original_img)
        self.draw_lines(self.the_line_array2, self.original_img)
        return cv2.resize(self.original_img, None, fx=0.9, fy=0.5)

    def return_img_points(self):
        self.draw_points(self.the_points_positions, self.original_img)
        return cv2.resize(self.original_img, None, fx=0.9, fy=0.5)




    def makes_lines_if_close_enogh(self, the_points_positions):
        #PRESITION_Y = 20
        #PRESITION_X = 75
        #LINE_LENGTH_REQURIMENT = 25

        the_line_array = []
        start_x = the_points_positions[0][0]
        start_y = the_points_positions[0][1]
        end_x = the_points_positions[0][0]
        end_y = the_points_positions[0][1]
        for i in range(len(the_points_positions)):
            current_x = the_points_positions[i][0]
            current_y = the_points_positions[i][1]
            if i != 0:
                prev_x = the_points_positions[i - 1][0]
            else:
                prev_x = the_points_positions[i][0]

            if abs(start_y - current_y) <= PRESITION_Y and abs(prev_x - current_x) <= PRESITION_X:
                if end_x < current_x:
                    end_x = current_x
                elif start_x > current_x:
                    start_x = current_x
                if end_y < current_y:
                    end_y = current_y

            elif (i + 1) == len(the_points_positions):
                the_line_array.append([(start_x, start_y), (end_x, end_y)])
            else:
                if abs(start_x - end_x) >= LINE_LENGTH_REQURIMENT:
                    the_line_array.append([(start_x, start_y), (end_x, end_y)])
                start_x = the_points_positions[i][0]
                start_y = the_points_positions[i][1]
                end_x = the_points_positions[i][0]
                end_y = the_points_positions[i][1]

        return the_line_array

class Edge_Detection():
    def __init__(self,img):
        self.img = img
        self.img_resize = cv2.resize(self.img, None, fx=0.5, fy=0.5)
        self.img_gray = cv2.cvtColor(self.img_resize, cv2.COLOR_BGR2GRAY)

        self.edges = cv2.Canny(self.img_gray, 100, 100)

        self.final_img = self.edges

    def return_img(self):
        return self.final_img


class Places_Boxes_On_Cha():

    def __init__(self, img, add_charecters=False):
        self.img = img
        self.hight, self.width = self.img.shape
        self.boxes = pytesseract.image_to_boxes(self.img)
        self.add_charecters = add_charecters
        for b in self.boxes.splitlines():
            b = b.split(" ")
            x,y,w,h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
            cv2.rectangle(self.img, (x,self.hight-y), (w,self.hight-h), (0,0,255),1)
            if self.add_charecters:
                cv2.putText(img, b[0], (x, self.hight-y), cv2.FONT_HERSHEY_COMPLEX,1, (50,50,255), 1)

    def return_img(self):
        return self.img

    def __str__(self):
        string = "Used for cheking error with the text generated by the image\n By placing boxes around each carekter"
        return string


class Reads_Img():
    def __init__(self, img):
        self.img = img
        self.text = pytesseract.image_to_string(img, lang="isl" )

    def returns_text(self):
        return self.text


#img_path = "Photos/photo5.jpg"
img_path = "Photos/photo6.jpg"
img = Loads_img(img_path).returns_img()
img_dot = Loads_img(img_path).returns_img()
img_lines = Loads_img(img_path).returns_img()

#img_lap = Edge_Detection(img).return_img()
#img_redeble = Makes_Img_Redeble(img).returns_img()

devided_img = Find_Lines(img).returns_devided_images()

#the devided images
for i in range(len(devided_img)):
    #the_image = cv2.resize(devided_img[i], None, fx =0.9, fy = 0.5)
    cv2.imshow(str(i+1),devided_img[i])


#img_boxes = Places_Boxes_On_Cha(img).return_img()

#the_sting = Reads_Img(img_redeble).returns_text()
#print(the_sting)

#cv2.imshow("results", img_redeble)

#the lines on the image
img_lines = Find_Lines(img).return_img_lines()
img_dots = Find_Lines(img_dot).return_img_points()
cv2.imshow("lines", img_lines)
cv2.imshow("Dots", img_dots)
plt.imshow(img_lines, cmap="gray", interpolation="bicubic")
plt.show()

cv2.waitKey(0)
cv2.destroyAllWindows()