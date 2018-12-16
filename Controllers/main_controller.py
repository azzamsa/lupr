import time
import getpass
import socket
import pathlib
import git
import os
from datetime import datetime
from subprocess import Popen, PIPE

from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QFileDialog, QMainWindow

RECORD_DIR = ""
FINISHED = pyqtSignal()

class MainController(QObject):
    def __init__(self, model):
        super().__init__()

        self._model = model

    def set_record_dir(self, dir_path):
        global RECORD_DIR
        RECORD_DIR = dir_path

    def print_record(self):
        print(str(RECORD_DIR) + " aku")

    def get_active_window_title():
        window_id_proc = Popen(['xprop', '-root', '_NET_ACTIVE_WINDOW'], stdout=PIPE)
        window_id, err = window_id_proc.communicate()
        for line in window_id.splitlines():
            window_id = line.split()[-1].decode()
            if window_id:
                window_name_proc = Popen(['xprop', '-id', window_id, 'WM_NAME'],
                                         stdout=PIPE)
                window_name, err = window_name_proc.communicate()
                return window_name.split()[-1].decode().strip('\"')


    def get_ip():
        ip = socket.gethostbyname(socket.gethostname())
        if ip == '127.0.1.1':
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("8.8.8.8", 80))
                ip = s.getsockname()[0]
                s.close()
            except Exception as e:
                ip = 'not connected to internet'

        return ip


    def get_all_windows():
        windows = ''
        proc = Popen(["wmctrl", "-l"], stdout=PIPE)
        out, err = proc.communicate()
        for line in out.splitlines():
            windows += line.split(None, 3)[-1].decode() + "\n"
        return windows


    def operate_git():
        if os.path.isdir('.git'):
            repo = git.Repo(RECORD_DIR)
        else:
            repo = git.Repo.init(RECORD_DIR)
            repo.config_writer().set_value("user", "name",
                                           getpass.getuser()).release()
            repo.config_writer().set_value("user", "email",
                                           socket.gethostname()).release()

        if "nothing to commit" not in str(repo.git.status()):
            repo.git.add('.')
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            repo.git.commit(m=now)


    def record(self):
        while True:
            self._model.write_auth_info()
            self._model.write_all_windows()
            self._model.write_focused_windows()
            self.operate_git()
            time.sleep(4 - time.time() % 4)
        self.FINISHED.emit()
