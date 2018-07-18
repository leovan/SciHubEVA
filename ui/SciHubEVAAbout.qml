import QtQuick 2.9
import QtQuick.Layouts 1.3
import QtQuick.Controls 2.2
import QtQuick.Window 2.3

Window {
    title: qsTr("About")
    modality: Qt.WindowModal

    property int margin: 10

    width: columnLayoutAbout.implicitWidth + 2 * margin
    height: columnLayoutAbout.implicitHeight + 2 * margin
    minimumWidth: columnLayoutAbout.Layout.minimumWidth + 2 * margin
    minimumHeight: columnLayoutAbout.Layout.minimumHeight + 2 * margin

    ColumnLayout {
        id: columnLayoutAbout
        anchors.fill: parent
        anchors.margins: margin

        RowLayout {
            id: rowLayoutAboutText
            spacing: 10
            Layout.fillWidth: true
            Layout.alignment: Qt.AlignLeft | Qt.AlignTop

            Image {
                id: imageAboutLogo
                Layout.alignment: Qt.AlignTop
                sourceSize.height: 89
                sourceSize.width: 43
                source: "qrc:/images/about.png"
            }

            TextArea {
                id: textAreaAboutText
                font.pointSize: 12
                Layout.fillWidth: true
                Layout.minimumWidth: 300
                onLinkActivated: Qt.openUrlExternally(link)
                Layout.alignment: Qt.AlignLeft | Qt.AlignTop
                textFormat: Text.RichText
                wrapMode: Text.WordWrap
                readOnly: true
                text: "<p><b>Sci-Hub EVA</b></p>" +
                      "<p>" + qsTr("Sci-Hub EVA is a cross-plotform Sci-Hub GUI Application.") + "</p>" +
                      "<p>" + qsTr("Author: ") + "<a href=\"https://leovan.me\">" + qsTr("Leo Van") + "</a></p>" +
                      "<p>" + qsTr("This application is licensed to you under ") +
                      "<a href=\"https://github.com/leovan/SciHubEVA\">The MIT License</a></p>"
            }
        }

        RowLayout {
            id: rowLayoutAboutButtons
            Layout.fillWidth: true
            Layout.alignment: Qt.AlignRight | Qt.AlignTop

            Button {
                id: aboutOKButton
                text: qsTr("OK")
                isDefault: true

                onClicked: close()
            }
        }
    }
}
