import os

from it.polimi.client import SshLaunch
from it.polimi.client import SshUpload
from it.polimi.client import checker
from it.polimi.client import sshDowload
from it.polimi.utils import IniManager


def print_menu():
    os.system('clear')
    print("____________Console for remote experiments____________\n")
    print("\t\t\t Menu \n")
    print("1) Check configuration file")
    print("2) Clean remote directory")
    print("3) Send experiment files")
    print("4) Run remote experiments")
    print("5) Check the status of remote experiments")
    print("6) Compress and download results")
    print("7) Fully automated experiments\n")
    print("8) Exit")


def select_from_menu():
    print_menu()
    while True:
        try:
            choice = int(input("Make your choice : "))
            print_menu()
            if 1 <= choice <= 8:
                break
        except:
            pass
    return choice


def check_conf():
    i_manager = IniManager(os.getcwd())
    i_manager.read_ini()


def clean_remote():
    i_manager = IniManager.IniManager(os.getcwd())
    i_manager.read_ini()
    uploader = SshUpload.FileUploader(i_manager)
    uploader.clean_remote()


def send_remote():
    i_manager = IniManager.IniManager(os.getcwd())
    i_manager.read_ini()
    uploader = SshUpload.FileUploader(i_manager)
    uploader.send()


def launch_remote():
    i_manager = IniManager.IniManager(os.getcwd())
    i_manager.read_ini()
    launcher = SshLaunch.ExpLauncher(i_manager)
    launcher.run()


def check_status():
    i_manager = IniManager.IniManager(os.getcwd())
    i_manager.read_ini()
    check = checker.StatusChecker(i_manager)
    check.start_checking()


def download():
    i_manager = IniManager.IniManager(os.getcwd())
    i_manager.read_ini()
    dl = sshDowload.Downloader(i_manager)
    dl.compress()
    dl.download_results()


def full_experiment():
    i_manager = IniManager.IniManager(os.getcwd())
    i_manager.read_ini()
    uploader = SshUpload.FileUploader(i_manager)
    uploader.clean_remote()
    uploader.send()
    launcher = SshLaunch.ExpLauncher(i_manager)
    launcher.run()
    check = checker.StatusChecker(i_manager)
    check.start_checking()
    dl = sshDowload.Downloader(i_manager)
    dl.compress()
    dl.download_results()


c = 0
while c != 8:
    c = select_from_menu()
    if c == 1:
        check_conf()
    if c == 2:
        clean_remote()
    if c == 3:
        send_remote()
    if c == 4:
        launch_remote()
    if c == 5:
        check_status()
    if c == 6:
        download()
    if c == 7:
        full_experiment()



