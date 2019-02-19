import time
from PyQt5.QtCore import QThread


class Recorder(QThread):
    """Worker thread to record all activity.
    App need multi thread in order to hang. """

    def __init__(self, model, controller):
        QThread.__init__(self)
        self._model = model
        self._main_ctrl = controller

    def __del__(self):
        self.wait()

    def run(self):
        while True:
            self._model.write_auth_info(self._main_ctrl.get_auth_info())
            self._model.write_all_windows(self._main_ctrl.get_all_windows())
            self._model.write_focused_window(
                self._main_ctrl.get_focused_window())
            self._main_ctrl.add_record()
            time.sleep(4 - time.time() % 4)
