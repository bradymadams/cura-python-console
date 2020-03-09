import QtQuick 2.7
import QtQuick.Controls 1.1
import QtQuick.Controls.Styles 1.1
import QtQuick.Layouts 1.1
import QtQuick.Dialogs 1.1
import QtQuick.Window 2.2

import UM 1.2 as UM

UM.Dialog {
    id: shellDialog
    title: "Ultimaker Cura | Python Shell"

    width: Math.floor(screenScaleFactor * 480)
    height: Math.floor(screenScaleFactor * 640)

    minimumWidth: Math.floor(screenScaleFactor * 320)
    minimumHeight: Math.floor(screenScaleFactor * 480)

    ColumnLayout {
        UM.I18nCatalog{id: catalog; name: "python-shell"}
        anchors.fill: parent
        anchors.margins: UM.Theme.getSize("default_margin").width

        spacing: UM.Theme.getSize("default_margin").height
        
        Button {
            Layout.alignment: Qt.AlignRight | Qt.AlignBottom

            text: catalog.i18nc("@action:button", "Close")
            onClicked: shellDialog.close()
        }
    }
}

