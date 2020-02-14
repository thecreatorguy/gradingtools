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

def move_provided_back_rec(home_path, temp_path):
    # Move files to location only if they don't already exist
    onlyfiles = [f for f in os.listdir(temp_path) if os.path.isfile(os.path.join(temp_path, f))]
    for filename in onlyfiles:
        home_file = os.path.join(home_path, filename)
        if not os.path.exists(home_file):
            temp_file = os.path.join(temp_path, filename)
            shutil.move(temp_file, home_file)

    # Move directories to location only if they don't already exist, keep track of existing directories
    existing_dirs = []
    onlydirs = [f for f in os.listdir(temp_path) if not os.path.isfile(os.path.join(temp_path, f))]
    for dirname in onlydirs:
        home_dir = os.path.join(home_path, dirname)
        if not os.path.exists(home_dir):
            temp_dir = os.path.join(temp_path, dirname)
            shutil.move(temp_dir, home_dir)
        else:
            existing_dirs.append(dirname)

    # For every existing directory, recursively check if there are existing files and move if not
    for existing_dir in existing_dirs:
        move_provided_back_rec(os.path.join(home_path, existing_dir), os.path.join(temp_path, existing_dir))

def move_provided(root, student_folder):
    os.chdir(student_folder)

    # Create temp
    home = os.getcwd()
    temp_dir = os.path.join(home, 'temp')
    if not os.path.exists(temp_dir):
        os.mkdir(temp_dir)

    # Move existing files to temp
    list_dir = os.listdir(home)
    for sub_dir in list_dir:
        dir_to_move = os.path.join(home, sub_dir)
        if dir_to_move != temp_dir:
            shutil.move(dir_to_move, temp_dir)

    # Copy provided files to folder
    copy_dir = os.path.join(home, '../../provided/' + root)
    for item in os.listdir(copy_dir):
        item_to_move = os.path.join(copy_dir, item)
        if os.path.isdir(item_to_move):
            shutil.copytree(item_to_move, os.path.join(home, item))
        else:
            shutil.copy(item_to_move, home)

    # Move folders and files out of temp and back to their original locations,
    # but only if it doesn't already exist
    move_provided_back_rec(home, temp_dir)

    # Delete temp
    shutil.rmtree(temp_dir)

    os.chdir('..')

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

        # There are only folders in the grading root now, save for later
        student_folders = [name for name in os.listdir()]

        shutil.copy('../provided/template.yaml', '%s.yaml' % root)
        print('Initialization complete. Make changes to yaml file and add provided files now')
        input('Press enter to continue...')

        for student_folder in student_folders:
            move_provided(root, student_folder)

        os.chdir('..')




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
