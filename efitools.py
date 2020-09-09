import os, re
from bcolors import bcolors

def find_EFI_partition():
    drive_list = os.popen('diskutil list').readlines()
    for line in drive_list:
        if 'EFI' in line and 'NO NAME' not in line:
            device = re.findall(r'disk.s.', line)
            return device[0]
    print(bcolors.FAIL + 'Couldn\'t find EFI partition. Aborting the program.' + bcolors.ENDC)
    exit()

def mount_EFI_partition(drive=None):
    if drive == None:
        drive = find_EFI_partition()
    if not os.path.exists('/Volumes/EFI'):
        os.system('sudo mkdir /Volumes/EFI')
        os.system('sudo mount -t msdos /dev/{} /Volumes/EFI'.format(drive))
    else:
        print(bcolors.FAIL + '\nDirectory ' + bcolors.BOLD + '/Volumes/EFI' + bcolors.ENDC + bcolors.FAIL + ' already exists.\n' + bcolors.ENDC)
        if len(os.listdir('/Volumes/EFI') ) != 0:
            print(bcolors.FAIL + bcolors.BOLD + '/Volumes/EFI' + bcolors.ENDC + bcolors.FAIL + ' is not empty!. Cancelling mount.\n' + bcolors.ENDC)
        else:
            os.system('sudo mount -t msdos /dev/{} /Volumes/EFI'.format(drive))

def unmount_EFI_partition(drive=None):
    if drive == None:
        drive = find_EFI_partition()
    os.system('sudo diskutil unmount /dev/{}'.format(drive))
