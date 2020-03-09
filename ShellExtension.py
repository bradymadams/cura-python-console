import os
import json

from PyQt5.QtCore import QUrl
from PyQt5.QtQml import qmlRegisterSingletonType
from PyQt5.QtQml import QQmlContext
from PyQt5.QtQml import QQmlComponent

from UM.i18n import i18nCatalog
from UM.Extension import Extension
from UM.Logger import Logger
from UM.PluginRegistry import PluginRegistry

from cura.CuraApplication import CuraApplication

i18n_catalog = i18nCatalog("python-shell")

class ShellExtension(Extension):
    def __init__(self):
        super().__init__()

        self._shell_window = None
        self.addMenuItem(i18n_catalog.i18nc("@item:inmenu", "Open in New Window"), self._openShellDialog)

        # About Dialog
        self._about_dialog = None
        self.addMenuItem(i18n_catalog.i18nc("@item:inmenu", "About"), self._openAboutDialog)

    def _createQmlDialog(self, dialog_qml, vars = None):
        directory = PluginRegistry.getInstance().getPluginPath(self.getPluginId())

        mainApp = CuraApplication.getInstance()

        return mainApp.createQmlComponent(os.path.join(directory, "qml", dialog_qml), vars)

    def _openAboutDialog(self):
        if not self._about_dialog:
            self._about_dialog = self._createQmlDialog("About.qml")
        #self._about_dialog.setParent(CuraApplication.getInstance().getMainWindow())
        self._about_dialog.show()

    def _closeAboutDialog(self):
        if not self._about_dialog:
            self._about_dialog.close()

    def _openShellDialog(self):
        if not self._shell_window:
            self._shell_window = self._createQmlDialog("ShellDialog.qml")
        self._shell_window.show()
