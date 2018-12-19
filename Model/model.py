from PyQt5.QtCore import QObject


class Model(QObject):
    def __init__(self):
        super().__init__()
        self._dir_path = ""

    def get_dir_path(self):
        return self._dir_path

    def set_dir_path(self, dir_path):
        self._dir_path = dir_path

    def get_file_path(self):
        return self._dir_path + "/.watchers"

    def write_auth_info(self, auth_info):
        auth_file = open(self.get_file_path() + "/auth_info", "w+")
        auth_file.write(auth_info)
        auth_file.close()

    def write_all_windows(self, all_windows):
        all_windows_file = open(self.get_file_path() + "/all_windows", "w+")
        all_windows_file.write(all_windows)
        all_windows_file.close()

    def write_focused_windows(self, active_window_title):
        focused_window_file = open(self.get_file_path() +
                                   "/focused_windows", "w+")
        focused_window_file.write(active_window_title)
        focused_window_file.close()
