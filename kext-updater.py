import webbrowser, os, sys
from bcolors import bcolors
from efitools import mount_EFI_partition, unmount_EFI_partition
from kext import get_installed_kexts, list_installed_kexts

def kext_manual_update(userfolder):
    path = userfolder + '/Downloads/Kexts'
    #webbrowser.open_new_tab('https://onedrive.live.com/?authkey=%21APjCyRpzoAKp4xs&id=FE4038DA929BFB23%21455036&cid=FE4038DA929BFB23')
    print(bcolors.OKGREEN + """Due to OneDrive API restrictions, kexts cannot be automatically downloaded, so you will have to do it manually.

A browser tab with the kext repository will open. Then, you have to check the listed kexts and see which ones might have an update (looking at the dates).

Download them and DONT EXTRACT THEM.

Once finished, press Return (Enter).""" + bcolors.ENDC)
    raw_input()
    files = []
    for filename in os.listdir('{}/Downloads'.format(userfolder)):
        if '.zip' in filename:
            files.append(filename)
    if len(files) == 0:
        print(bcolors.FAIL + '\nNo kexts found. Aborting' + bcolors.ENDC)
        return
    answer = raw_input('Kexts will be moved from {}/Downloads to {} folder, is this OK? [Y/n] '.format(userfolder,path))
    if answer.lower() == 'n':
        valid_path = 0
        print('\nIntroduce the full path to extract the kexts. Example: /Users/nick/Kexts...\n')
        path = raw_input('Path: ')
        while valid_path == 0:
            if path.startswith(userfolder):
                valid_path = 1
            else:
                print(bcolors.FAIL + '\nInvalid path. Try again\n' + bcolors.ENDC)
                path = raw_input('Path: ')
    if not os.path.exists(path):
        os.system('mkdir {}'.format(path))
    print('\nThe following files will be moved to {}'.format(path))
    for file in files:
        print(file)
        os.system('mv {}/Downloads/{} {}'.format(userfolder,file,path))
    extract_kexts(path)
    install_kexts(path)
    os.system('rm -rf {}'.format(path))

def extract_kexts(path):
    if len(os.listdir(path)) == 0:
        print(bcolors.WARNING + '\nNo kexts to extract.' + bcolors.ENDC)
        return
    for filename in os.listdir(path):
        if '.zip' in filename:
            print(bcolors.WARNING + '\nExtracting {}'.format(filename) + bcolors.ENDC)
            os.system('unzip {}/{} -d {}'.format(path,filename,path))
            os.system('rm {}/{}'.format(path,filename))

def install_kexts(path):
    if len(os.listdir(path)) == 0:
        print(bcolors.WARNING + '\nNo kexts to install.' + bcolors.ENDC)
        return
    for filename in os.listdir(path):
        if '.kext' in filename:
            if filename in os.listdir('/Volumes/EFI/EFI/OC/Kexts'):
                os.system('mv {}/{} /Volumes/EFI/EFI/OC/Kexts'.format(path,filename))
                print(bcolors.OKBLUE + '\nKext {} installed.'.format(filename) + bcolors.ENDC)
            else:
                answer = raw_input(bcolors.WARNING + '\nKext {} downloaded but not currently installed on system. Want to install anyway? [y/N] '.format(filename) + bcolors.ENDC)
                if answer.lower() == 'y':
                    os.system('mv {}/{} /Volumes/EFI/EFI/OC/Kexts'.format(path,filename))
                    print(bcolors.OKBLUE + '\nKext {} installed.'.format(filename) + bcolors.ENDC)

if __name__ == "__main__":
    if sys.platform != 'darwin':
        print(bcolors.FAIL + 'This script can only be used on '+ bcolors.BOLD + 'OS X' + bcolors.ENDC + bcolors.FAIL + ' systems. Shutting down' + bcolors.ENDC)
        exit()
    os.system('clear')
    print(bcolors.HEADER + '#'*20 + 'Kext Updater' + '#'*20 + bcolors.ENDC)
    mount_EFI_partition()
    kext_list = get_installed_kexts()
    list_installed_kexts(kext_list)
    kext_manual_update(os.path.expanduser('~'))
    unmount_EFI_partition()
