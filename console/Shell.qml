import QtQuick 2.4
import QtQuick.Controls 1.1
import QtQuick.Layouts 1.1
import QtQuick.Controls.Styles 1.1

import PythonConsole 1.0 as PythonConsole

TextArea {
    id: consoleTextArea

    property string startupScript

    PythonConsole.ShellInterface {
        id: shell
    }

    text: shell.text
    //textFormat: TextEdit.RichText

    style: TextAreaStyle {
        font.family: "Monospace"
        backgroundColor: "#222222"
        textColor: "#ebebeb"
    }

    Component.onCompleted: {
        var ran = shell.runScript(this.startupScript);
        if (!ran) {
            console.error("Failed to run startup script " + this.startupScript);
        }
        focus = true;
        cursorPosition = shell.adjustCursorPosition(0);
    }

    Keys.onPressed: {
        event.accepted = shell.keyPressed(event.key, event.modifiers, event.text);
        cursorPosition = 0
        text = shell.text
        cursorPosition = shell.cursorPosition
    }

    function mouseClick(mouse) {
        focus = true;
        cursorPosition = shell.adjustCursorPosition(
            positionAt(mouse.x, mouse.y)
        );
    }

    MouseArea {
        cursorShape: Qt.IBeamCursor;

        anchors.fill: parent;

        onClicked: {
            consoleTextArea.mouseClick(mouse);
        }
    }
}
