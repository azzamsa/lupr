from PyQt5.QtCore import QObject


class Model(QObject):
    def __init__(self):
        super().__init__()
        self._record_path = ""

    def get_record_path(self):
        """Return the value of record_path."""
        return self._record_path

    def set_record_path(self, record_path):
        """Set the value of record_path."""
        self._record_path = record_path

    def get_watcher_path(self):
        """Return the value of watchers."""
        return self._record_path + "/.watchers"

    def write_auth_info(self, auth_info):
        """Write auth information to file."""
        auth_file = open(self.get_watcher_path() + "/auth_info", "w+")
        auth_file.write(auth_info)
        auth_file.close()

    def write_all_windows(self, all_windows):
        """Write all windows title to file."""
        all_windows_file = open(self.get_watcher_path() + "/all_windows", "w+")
        all_windows_file.write(all_windows)
        all_windows_file.close()

    def write_focused_window(self, active_window):
        """Write focused window title to file."""
        focused_window_file = open(self.get_watcher_path() +
                                   "/focused_window", "w+")
        focused_window_file.write(active_window)
        focused_window_file.close()
