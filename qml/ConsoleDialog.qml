import QtQuick 2.7
import QtQuick.Controls 1.1
import QtQuick.Controls.Styles 1.1
import QtQuick.Layouts 1.1
import QtQuick.Dialogs 1.1
import QtQuick.Window 2.2

import UM 1.2 as UM

import PythonConsole 1.0 as PythonConsole

UM.Dialog {
    id: consoleDialog
    title: "Ultimaker Cura | Python Console"

    modality: Qt.NonModal;
    flags: Qt.Window;

    width: Math.floor(screenScaleFactor * 480)
    height: Math.floor(screenScaleFactor * 640)

    minimumWidth: Math.floor(screenScaleFactor * 320)
    minimumHeight: Math.floor(screenScaleFactor * 480)

    ColumnLayout {
        UM.I18nCatalog{id: catalog; name: "python-console"}
        anchors.fill: parent
        anchors.margins: UM.Theme.getSize("default_margin").width

        spacing: UM.Theme.getSize("default_margin").height

        PythonConsole.Shell {
            anchors.fill: parent
            anchors.bottomMargin: closeButton.height + UM.Theme.getSize("default_margin").height
        }

        Button {
            id: closeButton
            Layout.alignment: Qt.AlignRight | Qt.AlignBottom

            text: catalog.i18nc("@action:button", "Close")
            onClicked: consoleDialog.close()
        }
    }
}

