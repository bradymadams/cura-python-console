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

from PyQt5.QtCore import QUrl, QSize
from PyQt5.QtQml import QQmlApplicationEngine, QQmlComponent, QQmlContext
from PyQt5.QtGui import QIcon

def run():
    directory = os.path.dirname(os.path.abspath(__file__))

    appIcon = QIcon()
    appIcon.addFile(os.path.join(directory, "python.png"), QSize(64, 64))
    app.setWindowIcon(appIcon)

    from . import registerQmlTypes

    registerQmlTypes()

    engine = QQmlApplicationEngine()
    context = QQmlContext(engine)

    mainQml = QUrl.fromLocalFile(os.path.join(directory, 'Main.qml'))

    component = QQmlComponent(engine)
    component.loadUrl(mainQml)

    if component.isError():
        for error in component.errors():
            print('Error: ', error.toString())

    dialog = component.create(context)

    return app.exec_()

if __name__ == "__main__":
    sys.exit(run())
