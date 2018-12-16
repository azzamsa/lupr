from PyQt5.QtCore import QObject, pyqtSignal


class Model(QObject):
    def write_auth_info():
        auth_file = open(".watchers/auth_info", "w+")
        auth_file.write(getpass.getuser() + "\n")
        auth_file.write(socket.gethostname() + "\n")
        auth_file.write(get_ip())
        auth_file.close()

    def write_all_windows():
        all_windows_file = open(".watchers/all_windows", "w+")
        all_windows_file.write(get_all_windows())
        all_windows_file.close()


    def write_focused_windows():
        focused_window_file = open(".watchers/focused_windows", "w+")
        focused_window_file.write(get_active_window_title())
        focused_window_file.close()
