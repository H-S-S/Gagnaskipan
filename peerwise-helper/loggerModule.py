import os
from datetime import date

class loggerPeer:

    def __init__(self, log_name, log_info_list):
        self.file_name = 'loggFile.txt'
        self.log_name = log_name
        self.log_info_list = log_info_list

        self.main()

    def check_file_exists(self):
        return os.path.isfile(self.file_name)

    def append_to_file(self, info):
        file = open(self.file_name, 'a')
        file.write(info)
        file.close()

    def create_file(self):
        file = open(self.file_name, 'w')
        file.close()

    def main(self):
        if not self.check_file_exists:
            self.create_file()

        self.append_to_file('Log name: '+self.log_name)
        self.append_to_file(' (Date: ' + str(date.today())+ ')')
        self.append_to_file('\n')
        for i in range(len(self.log_info_list)):
            string = 'Page ' + str(i+1) + ' selected: ' + str(self.log_info_list[i])+'\n'
            self.append_to_file(string)

        self.append_to_file('\n')

        
#print(type(date.today()))
#print(str(type(date.today())))
    


