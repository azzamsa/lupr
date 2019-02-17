import getpass
import socket
import pathlib
import git
import os
from datetime import datetime
from subprocess import Popen, PIPE
from PyQt5.QtCore import QObject


class Controller(QObject):

    def __init__(self, model):
        super().__init__()

        self._model = model

    def set_record_dir(self, record_dir):
        self._model.set_record_dir(record_dir)
        self.create_record_dir()

    def get_active_window(self):
        window_id_proc = Popen(['xprop', '-root', '_NET_ACTIVE_WINDOW'],
                               stdout=PIPE)
        window_id, err = window_id_proc.communicate()
        for line in window_id.splitlines():
            window_id = line.split()[-1].decode()
            if window_id:
                window_name_proc = Popen(['xprop', '-id', window_id,
                                          'WM_NAME'], stdout=PIPE)
                window_name, err = window_name_proc.communicate()
                return " ".join(window_name.decode().split()[2:-1]) + "\n"

    def get_ip(self):
        ip = socket.gethostbyname(socket.gethostname())
        if ip == '127.0.1.1':
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("8.8.8.8", 80))
                ip = s.getsockname()[0]
                s.close()
            except Exception:
                ip = 'not connected to internet'

        return ip

    def get_all_windows(self):
        windows = ''
        proc = Popen(["wmctrl", "-l"], stdout=PIPE)
        out, err = proc.communicate()
        for line in out.splitlines():
            windows += line.split(None, 3)[-1].decode() + "\n"
        return windows

    def operate_git(self):
        record_dir = self._model.get_record_dir()
        if os.path.isdir(record_dir + '.git'):
            repo = git.Repo(record_dir)
        else:
            repo = git.Repo.init(record_dir)
            repo.config_writer().set_value("user", "name",
                                           getpass.getuser()).release()
            repo.config_writer().set_value("user", "email",
                                           socket.gethostname()).release()

        if "nothing to commit" not in str(repo.git.status()):
            repo.git.add('.')
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            repo.git.commit(m=now)

    def create_record_dir(self):
        pathlib.Path(self._model.get_record_dir() +
                     '/.watchers').mkdir(parents=True, exist_ok=True)

    def get_auth_info(self):
        auth_info = ""
        auth_info += getpass.getuser() + "\n"
        auth_info += socket.gethostname() + "\n"
        auth_info += self.get_ip() + "\n"
        return auth_info
