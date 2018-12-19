from PyQt5.QtCore import QObject


class Model(QObject):
    def __init__(self):
        super().__init__()
        self._record_dir = ""

    def get_record_dir(self):
        return self._record_dir

    def set_record_dir(self, record_dir):
        self._record_dir = record_dir

    def get_file_path(self):
        return self._record_dir + "/.watchers"

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
