import QtQuick 2.4
import QtQuick.Controls 1.1
import QtQuick.Layouts 1.1
import QtQuick.Controls.Styles 1.1

import UM 1.4 as UM
import Cura 1.1 as Cura

import PythonConsole 1.0 as PythonConsole

TextArea {
    PythonConsole.ShellInterface {
        id: shell
    }

    text: shell.text

    Keys.onPressed: {
        //console.log(event.key);
        event.accepted = shell.keyPressed(event.key, event.modifiers);
        text = shell.text
        cursorPosition = shell.cursorPosition
    }
}
