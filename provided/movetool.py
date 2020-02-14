import os
import sys
import shutil

def moveBackRec(home_path, temp_path):
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
        moveBackRec(os.path.join(home_path, existing_dir), os.path.join(temp_path, existing_dir))

def main():
    print('Moving Files')

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
    copy_dir = os.path.join(home, sys.argv[1])
    list_dir = os.listdir(copy_dir)
    for sub_dir in list_dir:
        dir_to_move = os.path.join(copy_dir, sub_dir)
        if os.path.isdir(dir_to_move):
            shutil.copytree(dir_to_move, os.path.join(home, sub_dir))
        else:
            shutil.copy(dir_to_move, home)

    # Move folders and files out of temp and back to their original locations,
    # but only if it doesn't already exist
    if len(sys.argv) > 2:
        moveBackRec(os.path.join(home, sys.argv[2]), temp_dir)
    else:
        moveBackRec(home, temp_dir)

    # Delete temp
    shutil.rmtree(temp_dir)

    print('Done!')

if __name__ == '__main__':
    main()