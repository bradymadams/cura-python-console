import os
import json

from PyQt5.Qt import Qt
from PyQt5.QtCore import pyqtProperty, pyqtSlot, QUrl, QObject
from PyQt5.QtQml import qmlRegisterSingletonType
from PyQt5.QtQml import QQmlContext
from PyQt5.QtQml import QQmlComponent

from UM.i18n import i18nCatalog
from UM.Extension import Extension
from UM.Logger import Logger
from UM.PluginRegistry import PluginRegistry

from cura.CuraApplication import CuraApplication

i18n_catalog = i18nCatalog("python-console")

class ConsoleExtension(Extension):
    def __init__(self):
        super().__init__()

        self._console_window = None
        self.addMenuItem(i18n_catalog.i18nc("@item:inmenu", "Open in New Window"), self._openConsoleDialog)

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

    def _openConsoleDialog(self):
        if not self._console_window:
            self._console_window = self._createQmlDialog("ConsoleDialog.qml")
        self._console_window.show()

class CodeLine:
    def __init__(self, code : str = None):
        self.code = code if code else ''
        self.active = True
        self.output = []

    def __iadd__(self, char : str):
        self.code += char
        return self

    def text(self, prompt):
        t = prompt + self.code
        if not self.active:
            t += '\n'
            for o in self.output:
                t += o + '\n'
        return t

class ShellInterface(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._prompt = ">>> "
        self._promptLength = len(self._prompt)

        self._enteredLines = [] # List[CodeLine]

        self._currentLine = CodeLine()
        self._cursor = 0

        self._oldLine = None

    @pyqtProperty(str)
    def text(self):
        t = ''.join([l.text(self._prompt) for l in self._enteredLines])
        t += self._currentLine.text(self._prompt)
        return t

    #@text.setter
    #def text(self, t : str):
    #    self._text = t

    @pyqtProperty(int)
    def cursorPosition(self):
        return self._cursor

    @pyqtSlot(int, int, result=bool)
    def keyPressed(self, key, modifiers):
        alt = False
        ctrl = False
        shift = False

        if modifiers:
            alt = bool(modifiers & Qt.AltModifier)
            ctrl = bool(modifiers & Qt.ControlModifier)
            shift = bool(modifiers & Qt.ShiftModifier)

            if alt or (shift and ctrl):
                return False

        if key == Qt.Key_Left:
            if self._cursor > 0:
                self._cursor -= 1
            return True

        if key == Qt.Key_Down:
            if self._oldLine:
                self._navigate(1)
            return True # we don't want to move the cursor - TODO how can we move it to EOL?

        if key == Qt.Key_Up:
            self._navigate(1)
            return True

        if key == Qt.Key_Right:
            # TODO check if cursor is at EOL and if so return True
            self._cursor += 1
            return True

        self._addCodeCharacter(key, shift)

        return True

    def _addCodeCharacter(self, key : int, shift : bool):
        # TODO need to check in cursor is not at EOL, so this would be an insertion
        self._currentLine += 'a'
        self._cursor += 1

    def _navigate(self, increment : int):
        pass
        # TODO
