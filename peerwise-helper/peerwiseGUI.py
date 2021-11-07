from os import name
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QLabel, QCheckBox, QHBoxLayout
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import pyqtSlot
import random
import loggerModule
import notChoseSamePagesTeem

class resultWindow(QMainWindow):
    def __init__(self, results):
        super(resultWindow, self).__init__()
        self.title = 'Peerwise Helper Results'
        #self.results = sorted(results)
        self.logged_info = False
        self.result_dic = results
        self.x = 0
        self.y = 0
        self.width = 600
        self.height = 600
        self.initUI()
        

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.x, self.y, self.width, self.height)

        base_lab_y = 50
        lab_between_y = 20
        base_lab_x = 20
        lab_between_x = 0
        
        pages_amount =0
        for book in self.result_dic:
            for _ in self.result_dic[book]:
                pages_amount+= 1
        lab_cordinates = [[base_lab_x, base_lab_y]]
        for i in range(1, pages_amount):
            lab_cordinates.append([lab_cordinates[i-1][0] + lab_between_x, lab_cordinates[i-1][1] + lab_between_y])

        
        self.questions_label = []
        qst_cnt = 0
        for book in self.result_dic:
            for i in range(len(self.result_dic[book])):
                string = 'Question ' + str(qst_cnt+1) + ' book: ' + book + ': page: ' + str(self.result_dic[book][i])
                self.questions_label.append(QLabel(self))
                self.questions_label[qst_cnt].setText(string)
            
                self.questions_label[qst_cnt].move(lab_cordinates[qst_cnt][0], lab_cordinates[qst_cnt][1])
                self.questions_label[qst_cnt].resize(450, 50)
                qst_cnt += 1
        
        
        self.lab_log = QLabel(self)
        self.lab_log.setText('Enter Log Name: ')
        self.lab_log.move(10, 10)
        self.lab_log.resize(150, 40)
        

        self.text_log = QLineEdit(self)
        self.text_log.move(170, 10)
        self.text_log.resize(200, 40)


        self.but_log = QPushButton('Log Pages', self)
        self.but_log.move(390, 10)
        self.but_log.resize(150, 40)
        self.but_log.clicked.connect(self.log_information)
    
        
        
        self.show()


    def log_information(self):
        if self.logged_info == False:
            log_name = str(self.text_log.text())
            result_list = []
            result_list_str = []
            for book in self.result_dic:
                for page in self.result_dic[book]:
                    result_list.append(page)
                    result_list_str.append(book +':'+ str(page))
            file = loggerModule.loggerPeer(log_name, result_list_str)
            notChoseSamePagesTeem.main(name='Hrafn', pages_list=result_list)
            self.logged_info = not self.logged_info


        
class peerWiseWindow(QMainWindow):
    def __init__(self, info_dic):
        super(peerWiseWindow, self).__init__()
        self.title = 'Peerwise Helper'
        self.info_dic = info_dic
        #self.RPi_book = self.info_dic['RPI-Book']
        #self.chapters_list = ['chapter8', 'chapter9', 'chapter10', 'chapter11', 'Actuators']
        #self.chapters_dic = {}
        #for chap in self.chapters_list:
        #    self.chapters_dic[chap] = self.RPi_book[chap]
        #print(self.chapters_dic)
        self.chapter_dic = {}
        for book in info_dic:
            self.chapter_dic[book] = []
            for chap in self.info_dic[book]:
                self.chapter_dic[book].append(chap)
        
        self.x = 0
        self.y = 0
        self.width = 800
        self.height = 800
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.x, self.y, self.width, self.height)
        

        # base_check_box_y = 50
        # check_box_between_y = 20
        # base_check_box_x = 20
        # check_box_between_x = 0
        
        # check_box_height = 20
        # check_box_width = 50

        
        #Adding book label for each book
        book_label_base_x = 20
        book_label_base_y = 20
        book_label_between_x = 20
        book_label_between_y = 0

        book_lab_size_x = 150
        book_lab_size_y = 20
        
        x_cont = book_label_base_x
        y_cont = book_label_base_y
        for book in self.info_dic:
            book_lab = QLabel(self)
            book_lab.setText(book)
            book_lab.move(x_cont, y_cont)
            x_cont += book_label_between_x + book_lab_size_x
            y_cont += book_label_between_y
            book_lab.resize(book_lab_size_x, book_lab_size_y)

        #adding the checkboxes under each book label
        self.check_box_dic = {}
        for book in self.info_dic:
            self.check_box_dic[book] = []
            for chap in self.info_dic[book]:
                self.check_box_dic[book].append(QCheckBox(chap, self))

        check_box_same_between_x = 0
        check_box_same_between_y = 20

        check_box_diff_between_x = book_lab_size_x + 20
        check_box_diff_between_y = 0

        check_base_x = book_label_base_x
        check_base_y = book_label_base_y + book_lab_size_y + 20

        x_cont = check_base_x
        y_cont = check_base_y
        for book in self.check_box_dic:
            for check in self.check_box_dic[book]:
                check.move(x_cont, y_cont)
                #x_cont += check_box_same_between_x
                y_cont += check_box_same_between_y
            
            x_cont += check_box_diff_between_x
            y_cont = check_box_diff_between_y + check_base_y



        self.gen_random_but = QPushButton("Generate Random Questions", self)
        self.gen_random_but.move((self.width-300-100), self.height - 40 - 10)
        self.gen_random_but.resize(300,30)
        self.gen_random_but.clicked.connect(self.gen_random_click)
        
        self.lab1 = QLabel(self)
        self.lab1.setText('Enter Number of Random questions')
        self.lab1.move(100, self.height -20 -50 -30)
        self.lab1.resize(350, 50)

        self.textbox1 = QLineEdit(self)
        self.textbox1.move(100, self.height -10 - 50)
        self.textbox1.resize(250, 50)

        self.show()

    def gen_random_click(self):
        #adds all the posible pages from each book into a dictionary
        self.checked_dic = {}
        for book in self.info_dic:
            self.checked_dic[book] = []
            for i in range(len(self.check_box_dic[book])):
                if self.check_box_dic[book][i].isChecked():
                    for ii in range(self.info_dic[book][self.chapter_dic[book][i]]['page range'][0], self.info_dic[book][self.chapter_dic[book][i]]['page range'][1]):
                        self.checked_dic[book].append(ii)
        
        #generates the random questions
        books =  []
        self.pages_dic = {}
        for book in self.info_dic:
            self.pages_dic[book] = []
            books.append(book)
        
        page_amount = 0
        self.num_rand_questions = int(self.textbox1.text())
        while page_amount < self.num_rand_questions:
            rand_book = random.randint(0, len(books)-1)
            rand_page = random.randint(0, len(self.checked_dic[books[rand_book]])-1)
            if self.checked_dic[books[rand_book]][rand_page] not in self.pages_dic[books[rand_book]]:
                self.pages_dic[books[rand_book]].append(self.checked_dic[books[rand_book]][rand_page])
                page_amount += 1





        # self.check_box_cheked = []
        # for i in range(len(self.check_box_list)):
        #     if self.check_box_list[i].isChecked():
        #         self.check_box_cheked.append(True)
        #     else:
        #         self.check_box_cheked.append(False)


        # self.pages = []
        # for i in range(len(self.check_box_cheked)):
        #     if self.check_box_cheked[i]:
        #         for ii in range(self.chapters_dic[self.chapters_list[i]]['page range'][0], self.chapters_dic[self.chapters_list[i]]['page range'][1]):
        #             self.pages.append(ii)

        # self.random_questions_pages = self.create_random_pages(self.pages)

        # #cheks what pages not to pick
        # self.not_chose_pages = []




        # for i in range(len(self.check_box_cheked)):
        #     if self.check_box_cheked[i]:
        #         for ii in range(len(self.chapters_dic[self.chapters_list[i][]]))

        self.answer_window = resultWindow(self.pages_dic)
        #self.close()
        self.answer_window.show()

    def create_random_pages(self, pages):
        print(pages)
        self.num_rand_questions = int(self.textbox1.text())
        teemates_questions = notChoseSamePagesTeem.main(name='Hrafn', only_get_teemates_pages=True)
        questions_page = []
        while len(questions_page) < self.num_rand_questions:
            rand_num = random.randint(0, len(pages))
            quest = pages[rand_num]
            if not quest in questions_page and not quest in teemates_questions:
                questions_page.append(quest)
        
        return questions_page

class selectBooks(QMainWindow):
    def __init__(self, books_info):
        super(peerWiseWindow, self).__init__()
        self.books_dic = books_info
        self.initUI()

    def initUI(self):
        pass

def run_main(info_dic):
    app = QApplication(sys.argv)
    #controlWindow = peerWiseWindow({'RPI-Book':{'chapter 8':{'page range': [310, 360]}, 'chapter 9':{'page range': [364, 402]}}})
    controlWindow = peerWiseWindow(info_dic)
    sys.exit(app.exec())

if __name__ == "__main__":
    run_main({'RPI-Book':{'chapter 8':{'page range': [310, 360]}, 'chapter 9':{'page range': [364, 402]}}})