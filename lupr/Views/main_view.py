import sys
from PyQt5.QtWidgets import QMenu, QSystemTrayIcon, QMainWindow, QFileDialog
from PyQt5.QtGui import QIcon
from Controllers.recorder import Recorder


class MainView(QMainWindow):
    def __init__(self, model, controller):
        super().__init__()

        self._model = model
        self._controller = controller

        # UI
        icon = QIcon("../lupr/Resources/img/lup.svg")
        menu = QMenu()
        record_action = menu.addAction("Start Recording")
        quit_action = menu.addAction("Stop and Quit")
        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(icon)
        self.tray.setContextMenu(menu)
        self.tray.show()
        self.tray.setToolTip("Lup")
        self.tray.showMessage("Lup", "Welcome to Lup", self.tray.Information,
                              1500)

        record_action.triggered.connect(self.record)
        quit_action.triggered.connect(self.quit_app)

        self.recorderThread = Recorder(model, controller)

    def save_record_path(self, record_path):
        "Save record path."
        self._controller.save_record_path(record_path)

    def choosedir_dialog(self, caption):
        """Prompts dialog to choose record directory."""
        options = (QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        return QFileDialog.getExistingDirectory(
            self, caption=caption, options=options)

    def record(self):
        """Start recording with worker(recorder) thread."""
        path = self.choosedir_dialog('Select Directory...')
        if not path:
            return None

        self.save_record_path(path)
        self.recorderThread.start()
        self.tray.showMessage("Lup", "Lup is recording", self.tray.Information,
                              1500)

    def quit_app(self):
        """Quit the app."""
        self.recorderThread.terminate()
        self.tray.showMessage("Lup", "See you")
        sys.exit()
