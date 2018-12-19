import time
import getpass
import socket
import pathlib
import git
import os
from datetime import datetime
from subprocess import Popen, PIPE
from PyQt5.QtCore import QObject, pyqtSignal


class MainController(QObject):

    def __init__(self, model):
        super().__init__()

        self._model = model

    def set_dir_path(self, dir_path):
        self._model.set_dir_path(dir_path)

    def get_active_window_title(self):
        window_id_proc = Popen(['xprop', '-root', '_NET_ACTIVE_WINDOW'],
                               stdout=PIPE)
        window_id, err = window_id_proc.communicate()
        for line in window_id.splitlines():
            window_id = line.split()[-1].decode()
            if window_id:
                window_name_proc = Popen(['xprop', '-id', window_id,
                                          'WM_NAME'], stdout=PIPE)
                window_name, err = window_name_proc.communicate()
                return window_name.split()[-1].decode().strip('\"')

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
        dir_path = self._model.get_record_dir()
        if os.path.isdir(dir_path + '.git'):
            repo = git.Repo(dir_path)
        else:
            repo = git.Repo.init(dir_path)
            repo.config_writer().set_value("user", "name",
                                           getpass.getuser()).release()
            repo.config_writer().set_value("user", "email",
                                           socket.gethostname()).release()

        if "nothing to commit" not in str(repo.git.status()):
            repo.git.add('.')
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            repo.git.commit(m=now)

    def create_dir(self):
        pathlib.Path(self._model.get_record_dir() +
                     '/.watchers').mkdir(parents=True, exist_ok=True)

    def get_auth_info(self):
        result = ""
        result += getpass.getuser() + "\n"
        result += socket.gethostname() + "\n"
        result += self.get_ip()
        return result

    def record(self):
        self.create_dir()
        while True:
            self._model.write_auth_info(self.get_auth_info())
            self._model.write_all_windows(self.get_all_windows())
            self._model.write_focused_windows(self.get_active_window_title())
            self.operate_git()
            time.sleep(4 - time.time() % 4)
            print("now is {}".format(time.time()))
        # self.FINISHED.emit()
