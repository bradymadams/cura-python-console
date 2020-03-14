import os
import sys

from PyQt5.QtCore import QUrl
from PyQt5.QtQml import qmlRegisterType, QQmlEngine, QQmlComponent

from UM.i18n import i18nCatalog
from UM.Logger import Logger

i18n_catalog = i18nCatalog("python-console")

from . import ConsoleExtension

def getMetaData():
    return {}


def register(app):
    directory = os.path.dirname(os.path.abspath(__file__))

    qmlRegisterType(
        ConsoleExtension.ShellInterface,
        "PythonConsole",
        1, 0,
        "ShellInterface"
    )

    qmlRegisterType(
        QUrl.fromLocalFile(os.path.join(directory, "qml", "Shell.qml")),
        "PythonConsole",
        1, 0,
        "Shell"
    )

    return {
        "extension": ConsoleExtension.ConsoleExtension(),
    }
