from it.polimi.command.sshServer import SSHManager


class StatusChecker:
    def __init__(self, ini_manager):
        self.__ini_manager = ini_manager

    def start_checking(self):
        print("____________Listening to remote experiments__________\n")
        server = SSHManager(self.__ini_manager)

        server_name, p, username = self.__ini_manager.get_connection_settings()
        command_list = ['bash']
        server.exec_command(command_list, option=False)
        command_list = ['pgrep -U ' + username + ' screen']

        ssh_output = server.exec_command(command_list, 4, False)
        output = ssh_output.split('\r')
        # print(output)
        num_screen = len(output)
        print('num experiments running: ' + str(num_screen - 3))

        while num_screen > 2:
            ssh_output = server.exec_command(command_list, 15, False)
            output = ssh_output.split('\r')
            # print(output)
            num_screen = len(output)
            print('num experiments running: ' + str(num_screen - 3))

        print("____________The experiments ended!____________")
        server.close()
