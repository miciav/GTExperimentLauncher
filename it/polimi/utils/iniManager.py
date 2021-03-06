import base64
import getpass
import os
from ConfigParser import ConfigParser


class IniManager:
    file_path = ''
    file_name = 'properties.ini'
    __full_file_name = ''
    config = ConfigParser()

    def __init__(self, path):
        self.file_path = path
        self.__full_file_name = self.file_path + '/' + self.file_name

    def __check_existence_ini(self):
        try:
            os.stat(self.__full_file_name)
        except Exception as e:
            print(e)
            config_file = open(self.__full_file_name, 'w')
            config_file.close()

    def __config_section_map(self, section):
        dict1 = {}
        options = self.config.options(section)
        for option in options:
            try:
                dict1[option] = self.config.get(section, option)
                if dict1[option] == -1:
                    print("skip: %s" % option)
            except:
                print("exception on %s!" % option)
                dict1[option] = None
        return dict1

    def __set_ini_field(self, section, name_field, encript):
        p = getpass.getpass(name_field + ': \n')
        if encript:
            enc64 = base64.b64encode(str.encode(p))
            enc = bytes.decode(enc64)
        else:
            enc = p
        self.config.set(section, name_field, enc)
        with open(self.__full_file_name, 'w') as configfile:
            self.config.write(configfile)

    def __set_ini_section(self, section):
        self.config.add_section(section)
        with open(self.__full_file_name, 'w') as configfile:
            self.config.write(configfile)

    def get_connection_settings(self):
        # type: () -> str, str
        fields = self.__config_section_map('connection settings')
        return fields.get('ip_server'), base64.b64decode(fields.get('password')), fields.get('username')

    def get_local_folder_name(self):
        fields = self.__config_section_map('general settings')
        return fields.get('folder_name')

    def get_remote_path(self):
        fields = self.__config_section_map('general settings')
        return os.getcwd(), fields.get('remote_path')

    def get_algo_list(self):
        fields = self.__config_section_map('general settings')
        return [x.strip() for x in fields.get('algo_list').split(',')]

    def get_phi_list(self):
        fields = self.__config_section_map('general settings')
        return [x.strip() for x in fields.get('phi_list').split(',')]

    def get_num_repetitions(self):
        fields = self.__config_section_map('general settings')
        return int(fields.get('num_repetitions'))

    def get_ni_info(self):
        fields = self.__config_section_map('general settings')
        return int(fields.get('max_ni')), int(fields.get('min_ni')), int(fields.get('increasing_step'))

    def get_experiment_name(self):
        fields = self.__config_section_map('general settings')
        return fields.get('experiment_name')

    def get_download_folder(self):
        fields = self.__config_section_map('general settings')

        return fields.get('download_folder')

    def read_ini(self):
        self.__check_existence_ini()
        self.config.read(self.__full_file_name)

        sections = self.config.sections()
        section = 'connection settings'
        if not sections.__contains__(section):
            self.__set_ini_section(section)

        fields = self.__config_section_map(section)
        server_name = fields.get('ip_server', 'empty')
        if server_name == 'empty' or server_name == '':
            self.__set_ini_field(section, 'ip_server', False)

        username = fields.get('username', 'empty')
        if username == 'empty' or username == '':
            self.__set_ini_field(section, 'username', False)

        password = fields.get('password', 'empty')
        if password == 'empty' or password == '':
            ris = raw_input('Is a password needed? (y/n) :')
            if ris == 'y':
                self.__set_ini_field(section, 'password', True)
            else:
                self.config.set(section, 'password', '')
                with open(self.__full_file_name, 'w') as configfile:
                    self.config.write(configfile)

        section = 'general settings'
        if not sections.__contains__(section):
            self.__set_ini_section(section)

        fields = self.__config_section_map(section)

        remote_path = fields.get('remote_path', 'empty')
        if remote_path == 'empty' or remote_path == '':
            self.__set_ini_field(section, 'remote_path', False)

        algo_list = fields.get('algo_list', 'empty')
        if algo_list == 'empty' or algo_list == '':
            self.__set_ini_field(section, 'algo_list', False)

        phi_list = fields.get('phi_list', 'empty')
        if phi_list == 'empty' or phi_list == '':
            self.__set_ini_field(section, 'phi_list', False)

        num_repetitions = fields.get('num_repetitions', 'empty')
        if num_repetitions == 'empty' or num_repetitions == '':
            self.__set_ini_field(section, 'num_repetitions', False)

        max_ni = fields.get('max_ni', 'empty')
        if max_ni == 'empty' or max_ni == '':
            self.__set_ini_field(section, 'max_ni', False)

        min_ni = fields.get('min_ni', 'empty')
        if min_ni == 'empty' or min_ni == '':
            self.__set_ini_field(section, 'min_ni', False)

        increasing_step = fields.get('increasing_step', 'empty')
        if increasing_step == 'empty' or increasing_step == '':
            self.__set_ini_field(section, 'increasing_step', False)

        experiment_name = fields.get('experiment_name', 'empty')
        if experiment_name == 'empty':
            ris = raw_input('Do you want to set a name for the experiment? (y/n) :\n')
            if ris == 'y':
                self.__set_ini_field(section, 'experiment_name', False)
            else:
                self.config.set(section, 'experiment_name', os.path.basename(os.getcwd()))
                with open(self.__full_file_name, 'w') as configfile:
                    self.config.write(configfile)
        folder_name = fields.get('folder_name', 'empty')
        if folder_name == 'empty' or folder_name == '':
            self.config.set(section, 'folder_name', os.path.basename(os.getcwd()))
            with open(self.__full_file_name, 'w') as configfile:
                self.config.write(configfile)

        download_folder = fields.get('download_folder', 'empty')
        if download_folder == 'empty':
            ris = raw_input('Do you want to set a download folder for the experiment? (y/n) :\n')
            if ris == 'y':
                self.__set_ini_field(section, 'download_folder', False)
            else:
                self.config.set(section, 'download_folder', os.path.basename(os.getcwd()))
                with open(self.__full_file_name, 'w') as configfile:
                    self.config.write(configfile)

       # print("Init file charged!")
