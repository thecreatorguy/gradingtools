#!/usr/bin/python3
"""
Filename: grade.py
Language: Python 3.6
Author: Timothy Johnson <tim@itstimjohnson.com>
Description: Runs the grading scripts
"""
import os
import zipfile
import shutil

from dotenv import load_dotenv
load_dotenv()

def init_grading_root(root):
    root_files = [name for name in os.listdir(root)]

    # The presence of the index will be our flag for having done our operations on this folder
    if 'index.html' in root_files:
        print('Initializing grading root...')
        os.chdir(root)
        os.remove('index.html')

        root_files.remove('index.html')
        for filename in root_files:
            temp = filename.replace(' ', '').split('-', 2)[2]       # Get after random number id
            student_name, original_filename = temp.rsplit('-', 1)
            os.mkdir(student_name)
            new_path = '%s/%s' % (student_name, original_filename)
            os.rename(filename, new_path)

            if filename.endswith('.zip'):
                with zipfile.ZipFile(new_path, 'r') as zip_ref:
                    zip_ref.extractall(student_name)
                os.remove(new_path)

        os.chdir('..')
        shutil.copy('provided/template.yaml', '%s/%s.yaml' % (root, root))

        print('Initialization complete. Make changes to yaml file and add provided files now')
        input('Press enter to continue...')

def main():
    dirs = [name for name in next(os.walk('.'))[1] if name not in os.getenv('GRADINGTOOLS_DIRECTORIES')]
    while True:
        for i, d in enumerate(dirs):
            print('[%2d] %s' % (i, d))
        choice = input('Select grading root: ')
        if not choice.isdigit():
            print('Choice was not in list.')
            continue
        choice = int(choice)
        if choice in range(len(dirs)):
            break
        print('Choice was not in list.')
    root = dirs[choice]
    init_grading_root(root)

    os.chdir('gradefast')
    os.system('python3 -m gradefast -f "../%s/" --shell "%s" "../%s/%s.yaml"' %
        (root, os.getenv('GRADEFAST_SHELL_PATH'), root, root))


if __name__ == '__main__':
    main()
