from it.polimi.client.sshServer import SSHManager


class Downloader:
    def __init__(self, ini_manager):
        self.__ini_manager = ini_manager

    def compress(self):
        print("____________Compressing remote files__________\n")
        server = SSHManager(self.__ini_manager)

        algo_list = self.__ini_manager.get_algo_list()

        # server, p, username = self.__ini_manager.get_connection_settings()
        experiment_name = self.__ini_manager.get_experiment_name()

        folders = 'test_folder'
        for a in algo_list:
            folders += '  ' + a + '_test_folder'

        server.exec_command(['tar -cvzf ' + experiment_name + '.tar.gz ' + folders], option=False)

        server.close()

    def download_results(self):
        print("____________Downloading results__________\n")
        server = SSHManager(self.__ini_manager)
        download_folder = self.__ini_manager.get_download_folder()
        if not download_folder.endswith("/"):
            download_folder += "/"
        experiment_name = self.__ini_manager.get_experiment_name();
        discard, remote_folder = self.__ini_manager.get_remote_path()
        if not remote_folder.endswith("/"):
            remote_folder += "/"
        server.get_file(download_folder + experiment_name + '.tar.gz', remote_folder + experiment_name + '.tar.gz')

