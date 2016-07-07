import os.path
import time

from paramiko import AutoAddPolicy, SSHClient


class SSHManager:
    @staticmethod
    def normalize_dirpath(dirpath):
        while dirpath.endswith("/"):
            dirpath = dirpath[:-1]
        return dirpath

    def __connect(self):
        server, p, username = self.__ini_manager.get_connection_settings()
        ssh = SSHClient()
        ssh.set_missing_host_key_policy(AutoAddPolicy())
        ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
        ssh.connect(server, username=username, password=p)
        return ssh

    def __init__(self, ini_manager):
        self.__ini_manager = ini_manager
        ssh_client = self.__connect()
        self.client = ssh_client
        self.channel = ssh_client.invoke_shell()

    def mkdir(self, sftp, remote_path, mode=0o777, intermediate=False):
        remote_path = self.normalize_dirpath(remote_path)
        if intermediate:
            try:
                sftp.mkdir(remote_path, mode=mode)
            except IOError:
                self.mkdir(sftp, remote_path.rsplit("/", 1)[0], mode=mode,
                           intermediate=True)
                return sftp.mkdir(remote_path, mode=mode)
        else:
            sftp.mkdir(remote_path, mode=mode)

    def get_file(self, local_path, remote_path):
        # normalize
        local_path = self.normalize_dirpath(local_path)
        remote_path = self.normalize_dirpath(remote_path)

        sftp = self.client.open_sftp()

        sftp.get(remote_path, local_path)

    def put_dir_recursively(self, local_path, remote_path, preserve_perm=True):
        """upload local directory to remote recursively"""

        assert remote_path.startswith("/"), "%s must be absolute path" % remote_path

        # normalize
        local_path = self.normalize_dirpath(local_path)
        remote_path = self.normalize_dirpath(remote_path)

        sftp = self.client.open_sftp()

        try:
            sftp.chdir(remote_path)
            local_suffix = local_path.rsplit("/", 1)[1]
            remote_suffix = remote_path.rsplit("/", 1)[1]
            if local_suffix != remote_suffix:
                remote_path = os.path.join(remote_path, local_suffix)
        except IOError as e:
            print(e)

        for root, dirs, fls in os.walk(local_path):
            prefix = os.path.commonprefix([local_path, root])
            suffix = root.split(prefix, 1)[1]
            if suffix.startswith("/"):
                suffix = suffix[1:]
            if not suffix.startswith("."):
                remroot = os.path.join(remote_path, suffix)

                try:
                    sftp.chdir(remroot)
                except IOError:
                    if preserve_perm:
                        mode = os.stat(root).st_mode & 0o777
                    else:
                        mode = 0o777
                    self.mkdir(sftp, remroot, mode=mode, intermediate=True)
                    sftp.chdir(remroot)
                try:
                    for f in fls:
                        rem_file = os.path.join(remroot, f)
                        local_file = os.path.join(root, f)
                        sftp.put(local_file, rem_file)
                        if preserve_perm:
                            sftp.chmod(rem_file, os.stat(local_file).st_mode & 0o777)
                except Exception as e:
                    print(e)

    def exec_command(self, command_list, wait_time=1, option=True):
        final_output = ''
        try:
            for c in command_list:
                self.channel.send(c + '\n')
                time.sleep(wait_time)
                output = self.channel.recv(5000)
                str_output = bytes.decode(output)
                if option:
                    print(str_output)
                final_output += ' ' + str_output
        except:
            pass
        return final_output

    def close(self):
        self.client.close()
