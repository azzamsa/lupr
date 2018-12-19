import time
from datetime import datetime
from PyQt5.QtCore import QThread


class Recorder(QThread):

    def __init__(self, model):
        QThread.__init__(self)
        self._model = model

    def __del__(self):
        self.wait()

    def run(self):
        while True:
            print("I am the loop")
            print(self._model.get_dir_path())
            time.sleep(4 - time.time() % 4)
            # QThread.sleep(4)
            print(datetime.now().strftime('%H:%M:%S'))
