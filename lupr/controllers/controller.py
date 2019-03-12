import getpass
import socket
import re
from subprocess import Popen, PIPE
from PyQt5.QtCore import QObject


class Controller(QObject):
    def __init__(self, model):
        super().__init__()

        self._model = model

    def set_record_path(self, record_path):
        """Set record path and create watchers dir."""
        self._model.record_path = record_path
        self._model.create_dotlup_dir()

    # @pyqtSlot(int)
    def change_interval(self, interval):
        self._model.record_interval = interval

    # FIXME crash when focused window has no title
    def get_focused_window(self):
        """Get current focused window title.

        window_name value is  b\'WM_NAME(STRING) = "WINDOW TITLE"\n'.
        WINDOW TITLE will be parsed using regex and returned as string.
        new line at the end of file needed as it's git convention.
        """
        window_id_proc = Popen(["xprop", "-root", "_NET_ACTIVE_WINDOW"], stdout=PIPE)
        window_id, err = window_id_proc.communicate()
        for line in window_id.splitlines():
            window_id = line.split()[-1].decode()
            if window_id:
                window_name_proc = Popen(
                    ["xprop", "-id", window_id, "WM_NAME"], stdout=PIPE
                )
                window_name, err = window_name_proc.communicate()
                focused_window = re.findall(r"\"(.+?)\"", window_name.decode())[0]
                return focused_window + "\n"

    def get_ip(self):
        """Get IP Address.

        Return 'Not connected' if no connection.
        """
        ip = socket.gethostbyname(socket.gethostname())
        if ip == "127.0.1.1":
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("8.8.8.8", 80))
                ip = s.getsockname()[0]
                s.close()
            except Exception:
                ip = "Not connected"

        return ip

    def get_all_windows(self):
        """Get all windows title.

        wmctrl result is 0x03800004  0 machine user - WINDOW TITLE.
        Window Title will be taken and returned as string.
        """
        windows = ""
        proc = Popen(["wmctrl", "-l"], stdout=PIPE)
        out, err = proc.communicate()
        for line in out.splitlines():
            windows += line.split(None, 3)[-1].decode() + "\n"
        return windows

    def get_auth_info(self):
        """Get auth information."""
        auth_info = ""
        auth_info += getpass.getuser() + "\n"
        auth_info += socket.gethostname() + "\n"
        auth_info += self.get_ip() + "\n"
        return auth_info
