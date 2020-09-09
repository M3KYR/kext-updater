import os, time, plistlib
from bcolors import bcolors

class Kext:
    def __init__(self,filename,filepath,version,date):
        self.filename = filename.replace('.kext', '')
        self.filepath = filepath
        self.version = version
        self.date = date

    def print_info(self):
        print('Name: {}'.format(self.filename.replace('.kext','')))
        print('Date: {}'.format(self.date))
        print('Version: {}\n'.format(self.version))

def get_installed_kexts():
    kext_list = []
    path = '/Volumes/EFI/EFI/OC/Kexts'
    if len(os.listdir(path)) == 0:
        print(bcolors.WARNING + 'No kexts found. Is the EFI partition mounted?' + bcolors.ENDC)
        return
    for kext in os.listdir(path):
        if not kext.startswith('.'):
            kextpath = os.path.join(path, kext)
            creation_time = time.ctime(os.stat(kextpath).st_ctime)
            kext_version = get_kext_version(kextpath)
            kext_list.append(Kext(kext,kextpath,kext_version,creation_time))
    return kext_list

def get_kext_version(kextpath):
    plist = plistlib.readPlist(kextpath + '/Contents/Info.plist')
    return plist['CFBundleVersion']

def list_installed_kexts(kext_list):
    for kext in kext_list:
        kext.print_info()
