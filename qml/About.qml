import QtQuick 2.7
import QtQuick.Controls 1.1
import QtQuick.Controls.Styles 1.1
import QtQuick.Layouts 1.1
import QtQuick.Dialogs 1.1
import QtQuick.Window 2.2

import UM 1.2 as UM

UM.Dialog {
    id: aboutDialog
    title: "Interactive Python Shell Plugin"

    width: Math.floor(screenScaleFactor * 400);
    minimumWidth: width;
    maximumWidth: width;

    height: Math.floor(screenScaleFactor * 350);
    minimumHeight: height;
    maximumHeight: height;

    ColumnLayout {
        UM.I18nCatalog{id: catalog; name: "python-shell"}
        anchors.fill: parent
        anchors.margins: UM.Theme.getSize("default_margin").width

        spacing: UM.Theme.getSize("default_margin").height

        Column {
            Layout.alignment: Qt.AlignCenter
            /*Image {
                width: Math.floor(screenScaleFactor * 300);
                
                fillMode: Image.PreserveAspectFit
                source: "images/branding.png"
                mipmap: true
            }*/
        }

        Text {
            Layout.alignment: Qt.AlignCenter
            
            //font: UM.Theme.getFont("default")
            font.underline: true
            color: "#0000ff"
            text: "Source Code"
            onLinkActivated: Qt.openUrlExternally(link)

            MouseArea {
                anchors.fill: parent
                hoverEnabled: true
                cursorShape: Qt.PointingHandCursor
                onClicked: Qt.openUrlExternally("https://github.com")
            }
        }
        
        Text {
            Layout.alignment: Qt.AlignCenter
            
            font: UM.Theme.getFont("default")
            color: UM.Theme.getColor("text")
            
            text: catalog.i18nc("@text", "")
        }
        
        Button {
            Layout.alignment: Qt.AlignCenter

            text: catalog.i18nc("@action:button", "Close")
            onClicked: aboutDialog.close()
        }
    }
}

