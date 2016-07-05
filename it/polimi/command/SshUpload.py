from __future__ import print_function
from __future__ import with_statement

import os
import time

import paramiko

import sshServer

"""
This is for uploading all the files.
"""


class file_uploader:
    def __init__(self, ini_manager):
        self.__ini_manager = ini_manager

    def __connect(self):
        server, p, username = self.__ini_manager.get_connection_settings()
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
        ssh.connect(server, username=username, password=p)
        return ssh

    def send(self):
        ssh = self.__connect();
        channel = ssh.invoke_shell()

        # invoke bash
        channel.send('bash\n')
        time.sleep(1)
        output = channel.recv(2024)
        print(output)

        # remove folders
        print("____________Removing remote Test Directory__________\n")
        channel.send('rm -rf ./GTExperimentLauncher\n')
        time.sleep(3)
        output = channel.recv(2024)
        print(output)


        print("____________Removing old execution folders___________\n")
        channel.send('rm -rf ./result_folder\n')
        time.sleep(4)
        output = channel.recv(2024)
        print(output)
        channel.send('rm -rf ./test_folder\n')
        time.sleep(4)
        output = channel.recv(2024)
        print(output)

        algo_list = self.__ini_manager.get_algo_list()
        for a in algo_list:
            channel.send('rm -rf ./{}_test_folder\n'.format(a))
            time.sleep(4)
            output = channel.recv(2024)
            print(output)

        try:
            server = sshServer.SSHManager(ssh)
            local_path, remote_path = self.__ini_manager.get_remote_path()

            print('____________Starting directory uploading____________\n')
            server.put_dir_recursively(local_path, remote_path)
            print('____________Directory uploading finished____________\n')

        except Exception as e:
            print("Ops, something went wrong!\n")
            ssh.close()
