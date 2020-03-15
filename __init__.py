from UM.i18n import i18nCatalog
from UM.Logger import Logger

from cura.CuraApplication import CuraApplication

i18n_catalog = i18nCatalog("python-console")

from . import console
from . import ConsoleExtension

_extension = ConsoleExtension.ConsoleExtension()

def getMetaData():
    return {}

def register(app):
    console.registerQmlTypes()

    CuraApplication.getInstance().initializationFinished.connect(
        _extension.applicationInitialized
    )

    return {
        "extension": _extension,
    }
