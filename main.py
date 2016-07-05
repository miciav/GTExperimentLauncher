import os

from it.polimi.command import SshUpload
from it.polimi.utils import iniManager

i_manager = iniManager.iniManager(os.getcwd())
i_manager.readIni()
uploader = SshUpload.file_uploader(i_manager)
uploader.send()
# the project copy itself on the server____________________________________

