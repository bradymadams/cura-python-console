import os
import sys

from UM.i18n import i18nCatalog
from UM.Logger import Logger

i18n_catalog = i18nCatalog("python-console")

from . import ConsoleExtension

def getMetaData():
    return {}


def register(app):
    return {
        "extension": ConsoleExtension.ConsoleExtension(),
    }
