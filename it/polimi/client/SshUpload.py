from __future__ import print_function
from __future__ import with_statement

import it.polimi.client.sshServer as sServer

"""
This is for uploading all the files.
"""


class FileUploader:
    def __init__(self, ini_manager):
        self.__ini_manager = ini_manager

    def clean_remote(self):
        server = sServer.SSHManager(self.__ini_manager)
        experiment_name = self.__ini_manager.get_experiment_name()
        print("____________Removing remote Test Directory__________\n")
        command_list = ['rm -rf ./' + experiment_name]
        server.exec_command(command_list, option=False)

        print("____________Removing old execution folders___________\n")
        command_list = ['rm -rf ./result_folder', 'rm -rf ./test_folder']

        algo_list = self.__ini_manager.get_algo_list()
        for a in algo_list:
            command_list.append('rm -rf ./{}_test_folder'.format(a))
        command_list.append('rm ' + experiment_name + '.tar.gz')

        server.exec_command(command_list, option=False)
        server.close()

    def send(self):
        server = sServer.SSHManager(self.__ini_manager)
        # send folders
        try:
            experiment_name = self.__ini_manager.get_experiment_name()
            local_path, remote_path = self.__ini_manager.get_remote_path()
            local_folder_name = self.__ini_manager.get_local_folder_name()
            print('____________Starting directory uploading____________\n')
            server.put_dir_recursively(local_path, remote_path)
            print('____________Directory uploading finished____________\n')
            if local_folder_name != experiment_name:
                server.exec_command(['mv {} {}'.format(local_folder_name, experiment_name)], option=False)
        except Exception as e:
            print(e)
            print("Ops, something went wrong!\n")

        server.close()
