
import os
import time

import paramiko

from paramiko.client import SSHClient
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
        algo_list = self.__ini_manager.get_algo_list()
        server, p, username = self.__ini_manager.get_connection_settings()
        channel = ssh.invoke_shell()
        channel.send('bash\n')
        time.sleep(1)
        output = channel.recv(2024)
        print(output)
        channel.send("kill $(pgrep -U "+username+" screen)\n")
        time.sleep(1)
        output = channel.recv(2024)
        print(output)
        channel.send('cd GTExperimentLauncher/it/polimi\n export PYTHONPATH=.\n')
        time.sleep(1)
        output = channel.recv(2024)
        print(output)
        channel.send('cd ../..\n ')
        time.sleep(1)
        output = channel.recv(2024)
        print(output)

        i = 0
        for a in algo_list:
            command = 'screen -S test_{} -d -m python it/polimi/server/run.py {} \n'.format(i, a)
            #command = 'python it/polimi/server/run.py {} \n'.format(a)
            print(command)
            channel.send(command)
            time.sleep(3)
            output = channel.recv(10000)
            print(output)
            i+=1

        channel.send('screen -S checker -d -m python it/polimi/server/executionChecker.py\n'.format(i))
        time.sleep(3)
        output = channel.recv(5000)
        print(output)

        # Close the connection
        ssh.close()
        print('Connection closed.')
        print("____________ The End______________________________\n")
