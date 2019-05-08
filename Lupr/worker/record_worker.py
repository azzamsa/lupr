import time
from PyQt5.QtCore import QThread


class RecordWorker(QThread):
    """Worker thread to record all activity.
    App need multi thread in order to hang. """

    def __init__(self, model, controller):
        QThread.__init__(self)
        self._model = model
        self._controller = controller

    def __del__(self):
        self.wait()

    def run(self):
        while True:
            auth_info = self._controller.get_auth_info()
            all_windows = self._controller.get_all_windows()
            focused_window = self._controller.get_focused_window()
            self._model.write_auth_info(auth_info)
            self._model.write_all_windows(all_windows)
            self._model.write_focused_window(focused_window)
            self._model.create_record()
            interval = self._model.record_interval
            time.sleep(interval - time.time() % interval)
