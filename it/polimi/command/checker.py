import paramiko
import time
import os

class statusChecker:
    def __init__(self, iniManager):
        self.__ini_manager = iniManager

    def __connect(self):
        server, p, username = self.__ini_manager.get_connection_settings()
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
        ssh.connect(server, username=username, password=p)
        return ssh

    def start_checking(self):
        ssh_client = self.__connect()
        channel = ssh_client.invoke_shell()
        server, p, username = self.__ini_manager.get_connection_settings()
        channel.send('bash\n')
        time.sleep(1)
        output = channel.recv(2024)
        print(output)
        channel.send("pgrep -U " + username + " screen\n")
        time.sleep(1)
        output= channel.recv(2024).split('\r')
        #print(output)
        num_screen = len(output)
        print('num experiments running: '+ str(num_screen-2))

        while num_screen >2:
            channel.send("pgrep -U " + username + " screen\n")
            time.sleep(15)
            output = channel.recv(2024).split('\n')
            #print(output)
            print('num experiments running: ' + str(num_screen - 2))
            num_screen = len(output)

        print("The experiment ended!")
        ssh_client.close()
