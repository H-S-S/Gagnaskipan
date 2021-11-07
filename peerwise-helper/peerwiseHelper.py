import random #imports random which comes with python when downloaded. 
import configparser
import ast
import argparse
import peerwiseGUI
import os


config_parse = configparser.ConfigParser()
config_parse.read('peerwiseHelper.ini')

# book_info = config_parse['RPI-Book']
# test2 = ast.literal_eval(book_info['chapters'])['chapter 9']
# test = ast.literal_eval(config_parse.get('RPI-Book', 'chapters'))
# print(test2)

books = ast.literal_eval(config_parse['all-books']['books'])

books_info = {}
for book in books:
    books_info[book] = {}
    bok_inf = ast.literal_eval(config_parse[book]['allChapters'])
    for chap in bok_inf:
        books_info[book][chap] = ast.literal_eval(config_parse[book][chap])

#print(books_info)



# #will remove start
# RPi_book_info = config_parse['RPI-Book']
# all_chapters_list = ast.literal_eval(RPi_book_info['allChapters'])

# info_dic = {
#     'RPI-Book':{}, }

# for chap in all_chapters_list:
#     info_dic['RPI-Book'][chap] = ast.literal_eval(RPi_book_info[chap])

#will remove end
parser = argparse.ArgumentParser()
parser.add_argument("--verbose", help="does not activate the GUI", action="store_true")

args = parser.parse_args()
if not args.verbose:
    #mainWindow = peerwiseGUI.run_main(info_dic)
    mainWindow = peerwiseGUI.run_main(books_info)
else:
    chapters_select = input('What chapters would you like (1 for chapter 1) use commas to seperate the chapters (1,2) => chapter 1 and 2 selected: ')
    chapter_select_list = chapters_select.split(',')
    chapter_name = []
    for chapt in chapter_select_list:
        string = 'chapter'+ str(chapt)
        chapter_name.append(string)
    
    
    all_pos_pages = []
    for chap_name in chapter_name:
        for i in range(info_dic['RPI-Book'][chap_name]['page range'][0], info_dic['RPI-Book'][chap_name]['page range'][1] + 1):
            all_pos_pages.append(i)
    
    num_questions = int(input('How many questions would you like to make?: '))
    questions_to_make_pages = []
    while len(questions_to_make_pages) < num_questions:
        rand_index = random.randint(0, len(all_pos_pages))
        quest_page = all_pos_pages[rand_index]
        if not quest_page in questions_to_make_pages:
            questions_to_make_pages.append(quest_page)

    for i in range(len(questions_to_make_pages)):
        print('Question {} will be on page: {}.'.format(i+1, questions_to_make_pages[i]))
    
    
    
    


'''
page_range = [160, 272]
#question_amount = int(input('How many questions would you like to write?: '))
question_amount = 3
skip_pages = [216, 217, 218, 219]
question_page = []
count = 0
while count<question_amount:
    n = random.randint(page_range[0], page_range[1])
    if not n in skip_pages and not n in question_page:
        question_page.append(n) 
        count+=1

question_page = sorted(question_page)
for i in range(0, len(question_page)):
    print('Question ' + str(i+1) + ' Will be on page: '+ str(question_page[i]))
'''

