import sys
import time
from PyQt5.QtWidgets import QApplication, QProgressBar, QSplashScreen
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

from Model.model import Model
from Controllers.main_controller import MainController
from Views.main_view import MainView


class App(QApplication):
    def __init__(self, sys_argv):
        super().__init__(sys_argv)
        self.model = Model()
        self.main_controller = MainController(self.model)
        self.main_view = MainView(self.model, self.main_controller)


if __name__ == "__main__":
    app = App(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    # Splash Screen
    splash_pix = QPixmap('../Lupr/Resources/img/lup-splash.svg')
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)

    progressBar = QProgressBar(splash)
    progressBar.setGeometry(0, 260, 700, 25)

    splash.setMask(splash_pix.mask())
    splash.show()

    for i in range(0, 100, 10):
        progressBar.setValue(i)
        t = time.time()
        while time.time() < t + 0.1:
            app.processEvents()

    time.sleep(1)
    splash.close()

    sys.exit(app.exec_())
