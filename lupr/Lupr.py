import sys
from PyQt5.QtWidgets import QApplication

from Model.model import Model
from Controllers.controller import Controller
from Views.main_view import MainView


class Lupr(QApplication):
    def __init__(self, sys_argv):
        super().__init__(sys_argv)
        self.model = Model()
        self.controller = Controller(self.model)
        self.main_view = MainView(self.model, self.controller)


if __name__ == "__main__":
    lupr = Lupr(sys.argv)
    lupr.setQuitOnLastWindowClosed(False)

    sys.exit(lupr.exec_())