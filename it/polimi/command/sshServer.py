import os.path


class SSHManager:
    @staticmethod
    def normalize_dirpath(dirpath):
        while dirpath.endswith("/"):
            dirpath = dirpath[:-1]
        return dirpath

    def __init__(self, sshClient):
        self.client = sshClient

    def mkdir(self, sftp, remote_path, mode=0777, intermediate=False):
        remote_path = self.normalize_dirpath(remote_path)
        if intermediate:
            try:
                sftp.mkdir(remote_path, mode=mode)
            except IOError as e:
                self.mkdir(sftp, remote_path.rsplit("/", 1)[0], mode=mode,
                           intermediate=True)
                return sftp.mkdir(remote_path, mode=mode)
        else:
            sftp.mkdir(remote_path, mode=mode)

    def put_dir_recursively(self, local_path, remote_path, preserve_perm=True):
        "upload local directory to remote recursively"

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
            pass

        for root, dirs, fls in os.walk(local_path):
            prefix = os.path.commonprefix([local_path, root])
            suffix = root.split(prefix, 1)[1]
            if suffix.startswith("/"):
                suffix = suffix[1:]

            remroot = os.path.join(remote_path, suffix)

            try:
                sftp.chdir(remroot)
            except IOError as e:
                if preserve_perm:
                    mode = os.stat(root).st_mode & 0777
                else:
                    mode = 0777
                self.mkdir(sftp, remroot, mode=mode, intermediate=True)
                sftp.chdir(remroot)

            for f in fls:
                remfile = os.path.join(remroot, f)
                localfile = os.path.join(root, f)
                sftp.put(localfile, remfile)
                if preserve_perm:
                    sftp.chmod(remfile, os.stat(localfile).st_mode & 0777)
