import ctypes
import ctypes.util

# https://stackoverflow.com/questions/39381009/simple-pyqt5-qml-application-causes-segmentation-fault
ctypes.CDLL(
    ctypes.util.find_library('GL'),
    ctypes.RTLD_GLOBAL
)

import sys
import os

from PyQt5.QtGui import QGuiApplication

app = QGuiApplication(sys.argv)

from PyQt5.QtCore import QUrl
from PyQt5.QtQml import QQmlApplicationEngine

def run():
    directory = os.path.dirname(os.path.abspath(__file__))

    from . import registerQmlTypes

    registerQmlTypes()

    mainQml = QUrl.fromLocalFile(os.path.join(directory, 'Main.qml'))
    engine = QQmlApplicationEngine(mainQml)

    return app.exec_()

if __name__ == "__main__":
    sys.exit(run())
