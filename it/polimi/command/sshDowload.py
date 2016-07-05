
import os
import time

import paramiko

class dowloader:

    def __init__(self, ini_manager):
        self.__ini_manager = ini_manager

    def __connect(self):
        server, p, username = self.__ini_manager.get_connection_settings()
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
        ssh.connect(server, username=username, password=p)
        return ssh

    def compress(self):
        print("____________Launching test using screen__________\n")

        ssh = self.__connect()
        #algo_list = self.__ini_manager.get_algo_list()
        #server, p, username = self.__ini_manager.get_connection_settings()
        channel = ssh.invoke_shell()
        channel.send('bash\n')
        time.sleep(1)
        output = channel.recv(2024)
        print(output)
        channel.send('tar -cvzf GTExperimentLauncher.tar.gz GTExperimentLauncher\n')
        time.sleep(1)
        output = channel.recv(2024)
        print(output)

        ssh.close()


