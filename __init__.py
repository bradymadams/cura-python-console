import os
import sys

from PyQt5.QtCore import QUrl
from PyQt5.QtQml import qmlRegisterType, QQmlEngine, QQmlComponent

from UM.i18n import i18nCatalog
from UM.Logger import Logger

i18n_catalog = i18nCatalog("python-console")

from . import console
from . import ConsoleExtension

def getMetaData():
    return {}

def register(app):
    console.registerQmlTypes()

    return {
        "extension": ConsoleExtension.ConsoleExtension(),
    }
