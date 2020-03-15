import QtQuick 2.7
import QtQuick.Controls 1.1
import QtQuick.Controls.Styles 1.1
import QtQuick.Layouts 1.1
import QtQuick.Dialogs 1.1
import QtQuick.Window 2.2

import PythonConsole 1.0 as PythonConsole

ApplicationWindow {
    id: mainWindow
    visible: true

    title: "Qt Python Console"

    width: 480
    height: 640

    minimumWidth: 320
    minimumHeight: 480

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 20

        spacing: 10

        PythonConsole.Shell {
            anchors.fill: parent
            anchors.bottomMargin: closeButton.height + 10
        }

        Button {
            id: closeButton
            Layout.alignment: Qt.AlignRight | Qt.AlignBottom

            text: "Close"
            onClicked: mainWindow.close()
        }
    }
}
