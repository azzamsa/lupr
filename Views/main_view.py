import sys
from PyQt5.QtWidgets import QMenu, QSystemTrayIcon, QMainWindow, QFileDialog
from PyQt5.QtGui import QIcon
from Controllers.recorder import Recorder


class MainView(QMainWindow):

    def __init__(self, model, main_controller):
        super().__init__()

        self._model = model
        self._main_controller = main_controller

        # UI
        icon = QIcon("../Lupr/Resources/img/lup.svg")
        menu = QMenu()
        record_action = menu.addAction("Start Recording")
        quit_action = menu.addAction("Stop and Quit")
        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(icon)
        self.tray.setContextMenu(menu)
        self.tray.show()
        self.tray.setToolTip("Lup")
        self.tray.showMessage("Lup", "Welcome to Lup",
                              self.tray.Information, 1500)

        record_action.triggered.connect(self.record)
        quit_action.triggered.connect(self.quit_app)

        self.recorderThread = Recorder(model, main_controller)

    def choose_record_dir(self):
        record_dir = str(QFileDialog.getExistingDirectory(self,
                                                          "Select Directory"))
        self._main_controller.set_record_dir(record_dir)

    def record(self):
        self.choose_record_dir()
        self.recorderThread.start()
        self.tray.showMessage("Lup", "Lup is recording",
                              self.tray.Information, 1500)

    def quit_app(self):
        self.recorderThread.terminate()
        self.tray.showMessage("Lup", "See you")
        sys.exit()
