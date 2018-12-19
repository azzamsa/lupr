import time
# from datetime import datetime
from PyQt5.QtCore import QThread


class Recorder(QThread):

    def __init__(self, model, main_controller):
        QThread.__init__(self)
        self._model = model
        self._main_ctrl = main_controller

    def __del__(self):
        self.wait()

    def run(self):
        while True:
            self._model.write_auth_info(self._main_ctrl.get_auth_info())
            self._model.write_all_windows(self._main_ctrl.get_all_windows())
            self._model.write_focused_windows(self._main_ctrl
                                              .get_active_window())
            self._main_ctrl.operate_git()
            time.sleep(4 - time.time() % 4)
            # print(self._model.get_record_dir())
            # print(datetime.now().strftime('%H:%M:%S'))
