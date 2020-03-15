from typing import List, Optional

import sys
import os
import code
import codeop
import io
import threading

from PyQt5.Qt import Qt
from PyQt5.QtCore import pyqtProperty, pyqtSlot, QUrl, QObject
from PyQt5.QtQml import qmlRegisterType

class CodeLine:
    def __init__(self, code : str = None):
        self.code = code if code else ''
        self.active = True
        self.output = []

    def __iadd__(self, char : str):
        self.code += char
        return self

    def insert(self, index : int, char : str):
        if index >= len(self.code):
            return
        if index == 0:
            self.code = char + self.code
        else:
            self.code = self.code[0:index] + char + self.code[index:]

    def delete(self, index : int):
        if index > len(self.code):
            return
        if index == 0:
            self.code = self.code[1:]
        else:
            self.code = self.code[0:index-1] + self.code[index:]

    def length(self):
        if self.active:
            return len(self.code)
        return len(self.code) + 1 + sum([len(o) + 1 for o in self.output])

    def text(self, prompt):
        t = prompt + self.code
        if not self.active:
            t += '\n'
            for o in self.output:
                t += o + '\n'
        return t

class CodeHistory:
    def __init__(self, prompt):
        self.maxLines = 100

        self._prompt = prompt
        self._lines = [] # List[CodeLine]
        self._nonEmptyLines = [] # List[CodeLine]

        self._cacheText = ''
        self._cacheLength = 0

        self._update()

    def _update(self):
        promptLength = len(self._prompt)
        self._cacheText = ''.join( [l.text(self._prompt) for l in reversed(self._lines)] )
        self._cacheLength = sum( (l.length() + promptLength) for l in self._lines )

    def add(self, line : CodeLine):
        if self.allLineCount() >= self.maxLines:
            rmline = self._lines.pop()

            # If the removed line is a non-empty line, need to remove
            # it in _nonEmptyLines as well
            if self.lineCount() > 0 and self._nonEmptyLines[-1] is rmline:
                self._nonEmptyLines.pop()

        # line is no longer active since it's being added to the history
        line.active = False
        self._lines.insert(0, line)

        # add it to _nonEmptyLines if it has code
        if len(line.code.strip()) > 0:
            self._nonEmptyLines.insert(0, line)

        self._update()

    def length(self):
        return self._cacheLength

    def text(self, prompt):
        return self._cacheText

    def lineCount(self) -> int:
        return len(self._nonEmptyLines)

    def allLineCount(self) -> int:
        return len(self._lines)

    def getLine(self, index) -> Optional[CodeLine]:
        '''
        Retrieve a CodeLine in the history. 0 is the most recent
        '''
        if index > len(self._nonEmptyLines):
            return None
        return self._nonEmptyLines[index]

class ShellInterface(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._interpreter = code.InteractiveInterpreter()
        self._compiler = codeop.CommandCompiler()

        self._prompt = ">>> "
        self._promptLength = len(self._prompt)

        self._history = CodeHistory(self._prompt)

        self._currentLine = CodeLine()
        self._cursor = 0

        self._historyLine = -1

        # keys to ignore and allow something else to handle
        # currently, we don't have any, so this may be removed
        self._passKeys = { }

        self._keyFunctions = {
            Qt.Key_Home: self._keyHome,
            Qt.Key_End: self._keyEnd,
            Qt.Key_Left: self._keyArrowLeft,
            Qt.Key_Right: self._keyArrowRight,
            Qt.Key_Down: self._keyArrowDown,
            Qt.Key_Up: self._keyArrowUp,
            Qt.Key_Enter: self._runCode,
            Qt.Key_Return: self._runCode
        }

    @pyqtProperty(str)
    def text(self):
        t = self._history.text(self._prompt)
        t += self._currentLine.text(self._prompt)
        return t

    #@text.setter
    #def text(self, t : str):
    #    self._text = t

    @pyqtProperty(int)
    def cursorPosition(self):
        return self._history.length() + self._promptLength + self._cursor

    @pyqtSlot(str, result=bool)
    def runScript(self, scriptPath):
        if len(scriptPath) == 0:
            return True
        if os.path.exists(scriptPath):
            with open(scriptPath, 'r') as fpy:
                lines = fpy.readlines()
            for line in lines:
                self._interpreter.runsource(line)
            return True
        return False

    @pyqtSlot(int, int, str, result=bool)
    def keyPressed(self, key, modifiers, text):
        alt = False
        ctrl = False
        shift = False

        if modifiers:
            alt = bool(modifiers & Qt.AltModifier)
            ctrl = bool(modifiers & Qt.ControlModifier)
            shift = bool(modifiers & Qt.ShiftModifier)

            if alt:
                # Do nothing when Alt is held down
                return True

            if ctrl:
                # Do nothing for now, but we need to check
                # for arrows and certain characters (e.g. V)
                # that we want to do stuff with
                return True

            if shift and ctrl:
                # Do nothing when Ctrl + Shift held down
                # TODO implement keyboard selection
                return True

        # Keys we pass on
        if key in self._passKeys:
            return False

        if key in self._keyFunctions.keys():
            self._keyFunctions[key]()
            return True

        if key in (Qt.Key_Backspace, Qt.Key_Delete):
            self._delCodeCharacter(key == Qt.Key_Backspace)

        if key >= Qt.Key_Space and key <= Qt.Key_AsciiTilde:
            self._addCodeCharacter(text)

        return True

    def _addCodeCharacter(self, text : str):
        if len(text) > 1:
            raise Exception("Cannot add more than one character to code line")

        if self._cursor < self._currentLine.length():
            self._currentLine.insert(self._cursor, text)
        else:
            self._currentLine += text

        self._cursor += 1

    def _delCodeCharacter(self, back):
        if back and self._cursor == 0:
            return
        elif not back and self._cursor == self._currentLine.length():
            return

        self._currentLine.delete(self._cursor if back else self._cursor + 1)

        if back:
            self._cursor -= 1

    def _runCode(self):
        _stdout = sys.stdout
        _stderr = sys.stderr
        _excepthook = sys.excepthook

        sstdout = sys.stdout = io.StringIO()
        sstderr = sys.stderr = io.StringIO()
        sys.excepthook = sys.__excepthook__

        try:
            code = self._compiler(self._currentLine.code)
        except (OverflowError, SyntaxError, ValueError):
            self._interpreter.showsyntaxerror()
        else:
            self._interpreter.runcode(code)

        sys.stdout = _stdout
        sys.stderr = _stderr
        sys.excepthook = _excepthook

        self._currentLine.output = \
            sstdout.getvalue().splitlines() + \
            sstderr.getvalue().splitlines()

        self._history.add(self._currentLine)
        self._currentLine = CodeLine()
        self._cursor = 0
        self._historyLine = -1

    def _keyHome(self):
        self._cursor = 0

    def _keyEnd(self):
        self._cursor = self._currentLine.length()

    def _keyArrowLeft(self):
        if self._cursor > 0:
            self._cursor -= 1

    def _keyArrowRight(self):
        n = self._currentLine.length()
        if self._cursor >= n:
            self._cursor = n
        else:
            self._cursor += 1

    def _keyArrowDown(self):
        self._navigateHistory(-1)

    def _keyArrowUp(self):
        self._navigateHistory(1)

    def _navigateHistory(self, increment : int):
        self._historyLine += increment
        self._historyLine = max(self._historyLine, -1)
        self._historyLine = min(self._historyLine, self._history.lineCount() - 1)
        if self._historyLine == -1:
            self._currentLine.code = ''
            self._cursor = 0
        else:
            line = self._history.getLine(self._historyLine)
            if line:
                self._currentLine.code = line.code
                self._keyEnd()

def registerQmlTypes():
    directory = os.path.dirname(os.path.abspath(__file__))

    qmlRegisterType(
        ShellInterface,
        "PythonConsole",
        1, 0,
        "ShellInterface"
    )

    qmlRegisterType(
        QUrl.fromLocalFile(os.path.join(directory, "Shell.qml")),
        "PythonConsole",
        1, 0,
        "Shell"
    )
