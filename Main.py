#!/usr/bin/env python3
import hashlib
from pathlib import Path
import shutil
import sys
import platform
import os
import string
from datetime import datetime

now = datetime.now() # current date and time
day = now.strftime("%d")
month = now.strftime("%m")
year = now.strftime("%Y")

date_append = '_('+day+'.'+month+'.'+year+')'
f1 = ''
username = ''
n_drives = 0
Total_file_size = 0
n_saves = 0
OS_String = 'Running on:'
win_drive_list = []
backup_dir = Path('Minecraft + Server', 'worlds [Java]')
user_blacklist = ['All Users','Default','Default User','desktop.ini','Public','Administrator']
save_dir = Path('.minecraft' , 'saves')
users_dir = ''
os_type = ''

def enter_to_exit(code = '0'):
    input("Press Enter to continue...")
    sys.exit(code)


def os_line():
    global os_type
    if os_type == 'Windows':
        return '-'*107
    elif os_type == 'Linux' or os_type == 'Darwin':
        return '-'*92
    else:
        return 0


def os_check():  # check for the operating system used
    global users_dir,os_type,save_dir,win_drive_list,drive_list
    for letter in string.ascii_uppercase:
        win_drive_list.append(letter+':')
    os_type =platform.system()
    if os_type == 'Linux': 
        users_dir = '/home'
        drive_list = os.listdir(Path('/media', username))
        #print('\n',os_line(),'\n',OS_String,'Linux\n',os_line(),'\n')
        #linux()
    elif os_type == "Windows":
        users_dir = 'C:/Users'
        save_dir =Path('Appdata', 'Roaming', save_dir)
        drive_list = win_drive_list
        #print("\n",os_line(),'\n',OS_String,'Windows\n',os_line(),'\n')
    elif os_type == 'Darwin':
        pass # insert mac os code here
    else:
        print(platform.system(), ': is not supported')
        enter_to_exit(1) ## Exit
    print("\n",os_line(),'\n',OS_String,platform.system(),platform.release(),'\n',os_line(),'\n')
    main()
    print("\n",os_line(),'\n')
    print('Backup Completed Successfully')
    if Total_file_size != 0 and n_drives != 0:
        print('Total', alt_file_check(Total_file_size / (n_drives / n_saves)), )
    else:
        print('Files are already up to date')
        enter_to_exit(0) ## Exit
    if n_drives != 0:
        print("Number of Backup Drives used:", n_drives / n_saves)
    else:
        print('No backup drives created/found')
    enter_to_exit(0) ## Exit

def main():# main program for bot windows and linux
    global users_dir,os_type,save_dir,n_saves,drive_list,n_drives
    pass
    for username in os.listdir(Path.home()): #loop through users directory
        os.chdir(Path.home())
        if username in user_blacklist:continue
        if not Path(Path.home(),username,save_dir).exists: # checks if save folder exists
            print('Minecraft Save folder not found...')
            enter_to_exit(1)
        if len(os.listdir(Path(Path.home(),username,save_dir))) == 0:#checks is save folder is empty
            print('Minecraft Save folder is empty...')
            enter_to_exit(1)
        os.chdir(Path(Path.home(),username,save_dir))# change directory to save directory
        for save in os.listdir(os.getcwd()):
            n_saves += 1
            md5 = md5_dir(save)
            for drive in drive_list:
                if not os.path.isdir(drive) and not os.path.isfile(drive):continue  # check if drive exists
                print('Found Drive:', drive)
                if not os.path.isdir(Path(drive, backup_dir)):  # check if backup directory exists
                    x = input('Do you want to create backup directory on drive: '+drive+' ?(Y/n)')
                    if x == 'Y' or x == 'y':
                        os.mkdir(Path(drive, backup_dir)) #make the backup directory
                    elif x == 'n' or x == 'N': continue #backup  folder not created by user so skip
                print('Found Backup directory')
                n_drives += 1
                backup_folder = Path(drive, backup_dir)
                backup_check(save,backup_folder,md5)


def backup_check(save,backup_folder,md5):
    if not os.path.exists(os.path.join(backup_folder, save + '.md5')):
        backup(save, backup_folder, md5)
    else:
        with open(os.path.join(backup_folder, save + '.md5'), 'r') as f:
            file_md5 = f.read()
        if file_md5 == md5: pass # if the file has not been changed skip
        else:
            backup(save, backup_folder, md5)

def backup(save, backup_folder, md5): # make a tar.gz archive and move it to backup location and make checksum file .md5
    shutil.make_archive(save, 'gztar', Path(os.getcwd(), save))
    if '_' in save:
        savename = save.split('_')
        new_filename = Path(savename[0] + date_append +'.minew')
        md5file = Path(savename[0] + date_append + '.md5')
        shutil.move(Path(os.getcwd(),save),Path(os.getcwd(),savename[0]+date_append))
    else:
        md5file = Path(save + date_append + '.md5')
        new_filename = Path(save + date_append + '.minew')
        shutil.move(Path(os.getcwd(),save),Path(os.getcwd(),save+date_append))
    os.rename(save + '.tar.gz', new_filename)
    shutil.move(new_filename, Path(backup_folder,new_filename))
    open(md5file, 'w+').write(str(md5))
    shutil.move(md5file, Path(backup_folder, md5file))
    print(file_size_check(Path(backup_folder, new_filename)))


def file_size_check(file_in):# returns the filesize
    global Total_file_size
    size = os.path.getsize(file_in)
    Total_file_size += size
    return alt_file_check(size)


def alt_file_check(rum):
    romlen = ''
    suffix = ''
    if rum < 1000:
        romlen = rum
        suffix = 'bytes'
    elif rum < 1000000:
        romlen = rum / 1024
        suffix = 'KiB'
    elif rum < 1000000000:
        romlen = rum / 1048576
        suffix = 'MiB'
    elif rum < 1000000000000:
        romlen = rum / 1073741824
        suffix = 'GiB'
    if romlen > 99:
        rumlen = str(romlen)[0:3]
    elif 99 > romlen > 10:
        rumlen = str(romlen)[0:2]
    else:
        rumlen = str(romlen)[0:1]
    return 'File Size: ' + rumlen + ' ' + suffix


def md5_update_from_dir(directory, hash):
    print(directory)
    assert Path(directory).is_dir()
    for path in sorted(Path(directory).iterdir(), key=lambda p: str(p).lower()):
        hash.update(path.name.encode())
        if path.is_file():
            with open(path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash.update(chunk)
        elif path.is_dir():
            hash = md5_update_from_dir(path, hash)
    return hash


def md5_dir(directory):
    return md5_update_from_dir(directory, hashlib.md5()).hexdigest()

if __name__ == '__main__':
    os_check()
