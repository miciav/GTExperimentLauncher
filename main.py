import os

from it.polimi.command import SshUpload
from it.polimi.utils import iniManager
from it.polimi.command import  SshLaunch
from it.polimi.command import checker
from it.polimi.command import  sshDowload

i_manager = iniManager.iniManager(os.getcwd())
i_manager.readIni()
uploader = SshUpload.file_uploader(i_manager)
uploader.send()
# the project copy itself on the server____________________________________

launcher = SshLaunch.ExpLauncher(i_manager)

launcher.run()

check = checker.statusChecker(i_manager)

check.start_checking()

dl = sshDowload.dowloader(i_manager)

dl.compress()
