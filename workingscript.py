import os
import shutil

def process(starting_dir, target_dir, fileName, difference):
    os.chdir(starting_dir)

    newName = fileName.split('.')[0] + difference +'.'+ fileName.split('.')[-1]

    print('THE WORKING DIRECTORY IS: '+ starting_dir)
    print('THE TARGET DIRECTORY IS: '+ target_dir)

    shutil.copy2(starting_dir + fileName, target_dir+newName)

    os.remove(starting_dir+fileName)
