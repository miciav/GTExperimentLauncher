from it.polimi.client.sshServer import SSHManager

"""
This is the script that launch all the experiments. 
It connects via SSH to the server, copies the data and launches the experiments in different screens

"""


class ExpLauncher:
    def __init__(self, ini_manager):
        self.__ini_manager = ini_manager

    def run(self):
        print("____________Launching test using screen__________\n")
        server = SSHManager(self.__ini_manager)

        algo_list = self.__ini_manager.get_algo_list()
        server_name, p, username = self.__ini_manager.get_connection_settings()
        experiment_name = self.__ini_manager.get_experiment_name()

        command_list = [
                        'kill $(pgrep -U ' + username + ' screen)',
                        'cd ' + experiment_name,
            'export PYTHONPATH=.',
            'cd it',
            'export PYTHONPATH=.',
            'cd polimi',
            'export PYTHONPATH=.',
                        'cd ../..']
        python_version = self.__ini_manager.get_remote_python_version()
        i = 0
        for a in algo_list:
            command = 'screen -S test_{} -d -m python{} it/polimi/server/runner.py {} \n'.format(i, python_version, a)
            command_list.append(command)
            i += 1

        command_list.append(
            'screen -S checker -d -m python{} it/polimi/server/executionChecker.py\n'.format(python_version))

        server.exec_command(command_list, option=True)
        server.close()
        print("____________ Experiments running___________________\n")
