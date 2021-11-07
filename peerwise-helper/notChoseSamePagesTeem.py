from git import Repo
import os
import csv


def get_file(repo):
    path = os.getcwd() + '/TeematesPages'
    try:
        Repo.clone_from(repo, path, single_branch=True, b='individual')
    except:
        pull_file(path)
    #file = open('/TeematesPages')
    return path

def push_file(path, file_name, commit_message):
    repo = Repo(path)
    repo.index.add([file_name])
    repo.index.commit(commit_message)
    origin = repo.remote(name='origin')
    origin.push()

def pull_file(path):
    repo = Repo(path)
    repo.remotes.origin.pull()

def get_file_content(path):
    with open(path, mode = 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        #csv_writer = csv.writer(csv_file)
        #headers = csv_reader.fieldnames
        headers = []
        headers = next(csv_reader)
        the_dics = {}
        for row in csv_reader:
            the_dics[row[0]] = list(map(int, row[1].split(' ')))
    
    return headers, the_dics


def make_line_inset(headers, dic, name, pages_list):
    dic[name] = pages_list
    lines_list = [headers]
    for na in dic:
        temp_list = [na]
        string = ''
        for pag in dic[na]:
            string += str(pag) + ' '
        string = string[:-1]
        temp_list.append(string)
        lines_list.append(temp_list)
    
    return lines_list



def change_csv(lines_list, path):
    with open(path, mode = 'w') as csv_file:
        csv_writer = csv.writer(csv_file)
        for line in lines_list:
            csv_writer.writerow(line)

def get_teemates_pages(my_name, the_dic):
    pages_list = []
    for name in the_dic:
        if name != my_name:
            for pag in the_dic[name]: 
                pages_list.append(pag)

    return pages_list
def main(name = '', pages_list = [], only_get_teemates_pages = False):
    if only_get_teemates_pages:
        path = get_file('git@github.com:ru-engineering/group-project-mech1-03.git')
        headers, the_dic = get_file_content('TeematesPages/peerwise2.csv')
        return get_teemates_pages(name, the_dic)
    else:
        path = get_file('git@github.com:ru-engineering/group-project-mech1-03.git')
        headers, the_dic = get_file_content('TeematesPages/peerwise2.csv')
        the_lines = make_line_inset(headers, the_dic, name, pages_list)
        change_csv(the_lines, 'TeematesPages/peerwise2.csv')
        push_file(path, 'peerwise2.csv', 'Hrafns Pages')



if __name__ == '__main__':
    main(name='Hrafn', pages_list=[0, 0, 0])