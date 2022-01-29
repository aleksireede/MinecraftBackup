import hashlib
import os
import shutil
import sys
import traceback

f1 = ''
linux_line = '-'*92
windows_line = '-'*107
username = ''
number_of_drives = 0
Total_file_size = 0
number_of_saves = 0
OS_String = 'Your Operating system is:'
drive_list = ['A:', 'B:', 'D:', 'E:', 'F:', 'G:', 'H:', 'I:', 'J:', 'K:', 'L:', 'M:', 'N:', 'O:', 'P:', 'Q:', 'R:',
              'S:', 'T:', 'U:', 'V:', 'W:', 'X:', 'Y:', 'Z:']


def os_check():  # check for the operating system used
    if sys.platform == "linux" or sys.platform == "linux2":
        print('\n',linux_line,OS_String,'Linux',linux_line,'\n')
        linux()
        print('\n',linux_line,'\n')
    elif sys.platform == "win32":
        print("\n",windows_line,OS_String,'Windows',windows_line,'\n')
        windows()
        print("\n",windows_line,'\n')
    else:
        print(sys.platform, ': is not supported')
        input('Press Enter to continue:')
        sys.exit(1)
    print('Backup Completed Successfully')
    if Total_file_size != 0 and number_of_drives != 0:
        print('Total', alt_file_check(Total_file_size / (number_of_drives / number_of_saves)), )
    else:
        print('Files are already up to date')
        input("Press Enter to continue...")
        sys.exit(1)
    if number_of_drives != 0:
        print("Number of Backup Drives used:", number_of_drives / number_of_saves)
    else:
        print('No backup drives created/found')
    input("Press Enter to continue...")
    sys.exit(1)


def windows():
    global number_of_drives, Total_file_size, number_of_saves
    for user in os.listdir('C:/Users'):  # check for users
        os.chdir('C:/Users')  # change directory to users dir
        if user != 'All Users' and user != 'Default' and user != 'Default User' and user != 'desktop.ini' \
                and user != 'Public':
            print('Found User:', user)  # real user found
            if os.path.exists(os.path.join('C://', 'Users', user, 'Appdata', 'Roaming', '.minecraft', \
                                           'MainSurvival', 'saves')):  # check if save directory exists
                os.chdir(
                    os.path.join(user, 'Appdata', 'Roaming', '.minecraft', \
                                 'MainSurvival', 'saves'))  # change directory to save directory
                for save in os.listdir(os.getcwd()):  # do for every save
                    number_of_saves += 1
                    md5 = get_dir_hash(save, 0)  # calculate save md5 hash
                    for drive in drive_list:  # search for backup drives
                        if not os.path.exists(drive):  # check if drive exists
                            continue
                        print('Found Drive:', drive)
                        if not os.path.exists(os.path.join(drive, 'Minecraft + Server', 'worlds [Java]')):  # check if backup directory exists
                            x = input('Do you want to create backup directory? (Y/n)')
                            if x == 'Y' or x == 'y':
                                os.mkdir(os.path.join(drive, 'Minecraft + Server', 'worlds [Java]'))
                            elif x == 'n' or x == 'N':
                                pass
                            continue
                        print('Found Backup directory')
                        number_of_drives += 1
                        backup_folder = os.path.join(drive, 'Minecraft + Server', 'worlds [Java]')
                        with open(os.path.join(backup_folder, save + '.md5'), 'r') as f:
                            file_md5 = f.read()
                        if file_md5 == md5:
                            continue
                        backup(save, backup_folder, md5)
                        


def linux():
    global number_of_drives, Total_file_size, number_of_saves, username
    for user in os.listdir('/home'):  # check fo users
        os.chdir(os.path.join('/home', user))  # change directory to /home/username
        print('Found user:', user)
        username = user
        if os.path.exists(os.path.join('/home', user, '.minecraft', 'saves')):  # check if the user has installed minecraft correctly
            print('Found Minecraft Installation')
            os.chdir(os.path.join('/home', user, '.minecraft', 'Mainsurvival', 'saves'))
            for save in os.listdir(os.getcwd()):  # do for every save in saves directory
                print('Found world save:', save)
                number_of_saves += 1  # add one number to number of saves
                md5 = get_dir_hash(save, 0)  # calculate md5 checksum of save
                for drive in os.listdir(os.path.join('/media', username)):  # check every drive mounted
                    print('Found drive:', drive)
                    if os.path.exists(os.path.join('/media', username, drive, 'Minecraft + Server', 'worlds [Java]')):
                        print('Found backup folder on drive')
                        number_of_drives += 1
                        backup_folder = os.path.join('/media', username, drive, 'Minecraft + Server', 'worlds [Java]')
                        with open(os.path.join(backup_folder, save + '.md5'), 'r') as f:
                            file_md5 = f.read()
                        if file_md5 == md5:
                            continue
                        else:
                            backup(save, backup_folder ,md5)
                    else:
                        x = input('Do you want to create backup directory? (Y/n)')
                        if x == 'Y' or x == 'y':
                            os.mkdir(os.path.join('/media', username, drive, 'Minecraft + Server', 'worlds [Java]'))
                        elif x == 'n' or x == 'N':
                            pass
        elif os.path.exists(os.path.join('/home', user, '.minecraft')):
            print('Minecraft Installation is Incomplete')
        else:
            print('No minecraft installation found')


def backup(save, backup_folder, md5):
    shutil.make_archive(save, 'zip', os.path.join(os.getcwd(), save))
    os.rename(save + '.zip', save + '.minew')
    shutil.move(save + '.minew', os.path.join(backup_folder, save + '.minew'))
    with open(save + '.md5', 'w') as file:
        file.write(md5)
    shutil.move(save + '.md5', os.path.join(backup_folder, save + '.md5'))
    print(file_size_check(os.path.join(backup_folder, save + '.minew')))


def file_size_check(file_in):
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


def get_dir_hash(directory, verbose=0):
    global f1
    sha_hash = hashlib.md5()
    if not os.path.exists(directory):
        return -1
    try:
        for root, dirs, files in os.walk(directory):
            for names in files:
                if verbose == 1:
                    print('Hashing', names)
                filepath = os.path.join(root, names)
                try:
                    f1 = open(filepath, 'rb')
                except:
                    # You can't open the file for some reason
                    f1.close()
                    continue
                while 1:
                    # Read file in as little chunks
                    buf = f1.read(4096)
                    if not buf:
                        break
                    sha_hash.update(hashlib.md5(buf).digest())
                f1.close()
    except:
        # Print the stack traceback
        traceback.print_exc()
        return -2
    return sha_hash.hexdigest()


if __name__ == '__main__':
    os_check()
