from __future__ import print_function
from __future__ import with_statement

import os
import time

import paramiko

from it.polimi.server import fileUtils

"""
This is the script that launch all the experiments. 
It connects via SSH to the server, copies the data and launches the experiments in different screens

"""


class ExpLauncher:

    def __init__(self, ini_manager):
        self.__ini_manager = ini_manager

    def __connect(self):
        server, p, username = self.__ini_manager.get_connection_settings()
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
        ssh.connect(server, username=username, password=p)
        return ssh

    def run(self):
        print("____________Launching test using screen__________\n")
        ssh = self.__connect()

        channel = ssh.invoke_shell()
        channel.send('bash\n')
        time.sleep(1)
        output = channel.recv(2024)
        print(output)
        channel.send('cd server/\n')
        time.sleep(1)
        output = channel.recv(2024)
        print(output)
        channel.send('screen -S test_2 -d -m python run.py alg2_1\n')
        time.sleep(3)
        output = channel.recv(5000)
        print(output)
        channel.send('screen -S test_2 -d -m python run.py alg2_2\n')
        time.sleep(3)
        output = channel.recv(5000)
        print(output)
        channel.send('screen -S test_2 -d -m python run.py alg2_3\n')
        time.sleep(3)
        output = channel.recv(5000)
        print(output)
        channel.send('screen -S test_2 -d -m python executionChecker.py\n')
        time.sleep(3)
        output = channel.recv(5000)
        print(output)

        # Close the connection
        ssh.close()
        print('Connection closed.')
        print("____________ The End______________________________\n")
