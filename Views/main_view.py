from PyQt5.QtWidgets import QMenu, QSystemTrayIcon, QMainWindow, QFileDialog
from PyQt5 import QtGui
import sys


class MainView(QMainWindow):
    def __init__(self, model, main_controller):
        super().__init__()

        self._model = model
        self._main_controller = main_controller

        # UI
        icon = QtGui.QIcon("../Cornear/Resources/img/icon24x24.png")
        menu = QMenu()
        choose_dir_action = menu.addAction("Start Recording")
        stop_action = menu.addAction("Stop Recording")

        self.tray = QSystemTrayIcon()
        self.tray.setIcon(icon)
        self.tray.setContextMenu(menu)
        self.tray.show()
        self.tray.setToolTip("Cornea")
        self.tray.showMessage("Recording Started", "Cornea is recording")

        # connect widgets to controller
        choose_dir_action.triggered.connect(self.choose_dir)
        stop_action.triggered.connect(self.close)

    def choose_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Directory")
        self._main_controller.set_record_dir(dir_path)
        # self._main_controller.print_record()
