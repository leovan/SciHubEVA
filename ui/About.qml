import QtQuick 2.14
import QtQuick.Layouts 1.14
import QtQuick.Controls 2.14
import QtQuick.Window 2.14
import QtQuick.Controls.Material 2.14

Dialog {
    x: (parent.width - width) / 2
    y: (parent.height - height) / 2

    modal: true

    ColumnLayout {
        id: columnLayoutAbout

        anchors.fill: parent

        RowLayout {
            id: rowLayoutAboutText

            spacing: 20

            Image {
                id: imageAboutLogo

                Layout.alignment: Qt.AlignTop

                sourceSize.height: 86
                sourceSize.width: 86
                source: "qrc:/images/SciHubEVA-icon.png"
            }

            Label {
                id: labelAboutText
                text: "<style>a { color: " + Material.accent + "; }</style>" +
                      "<p><b>Sci-Hub EVA v4.0.1</b></p>" +
                      "<p>" + qsTr("Sci-Hub EVA is a cross-platform Sci-Hub GUI Application based on ") +
                      "Python " + PYTHON_VERSION + qsTr(" and ") +
                      "Qt (PySide2) " + QT_VERSION + qsTr(".") + "</p>" +
                      "<p>" + qsTr("Author: ") + "<a href=\"https://leovan.me\">" + qsTr("Leo Van") + "</a><br/>" +
                      qsTr("License: ") + "<a href=\"https://github.com/leovan/SciHubEVA\">The MIT License</a>" +
                      "</p>"

                Layout.preferredWidth: 300
                Layout.maximumWidth: 300

                onLinkActivated: Qt.openUrlExternally(link)
                textFormat: Text.RichText
                wrapMode: Text.WordWrap
            }
        }
    }
}
