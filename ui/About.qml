import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
import QtQuick.Window
import QtQuick.Controls.Material

Dialog {
    id: dialog

    x: (parent.width - width) / 2
    y: (parent.height - height) / 2

    modal: true

    Material.roundedScale: Material.SmallScale

    ColumnLayout {
        anchors.fill: parent

        RowLayout {
            Layout.fillWidth: true

            spacing: 8

            Image {
                Layout.alignment: Qt.AlignTop

                sourceSize.height: 128
                sourceSize.width: 128
                source: "qrc:/images/SciHubEVA-icon.png"
            }

            Label {
                text: "<style>a { color: " + Material.accent + "; }</style>" +
                      "<p><b>Sci-Hub EVA</a> " + APPLICATION_VERSION + "</b></p>" +
                      "<p>" + "<a href=\"https://github.com/leovan/SciHubEVA\">Sci-Hub EVA</a> " +
                      qsTr("is a cross-platform Sci-Hub GUI Application.") + "<br/>" +
                      "Powered By Python " + PYTHON_VERSION + " & Qt " + QT_VERSION + "</p>" +
                      "<p>Copyright (c) 2018-2023 <a href=\"https://leovan.me\">" + qsTr("Leo Van") +
                      "</a> The MIT License</p>"

                Layout.fillWidth: true
                Layout.minimumWidth: 200

                textFormat: Text.RichText
                wrapMode: Text.WordWrap

                onLinkActivated: (link) => {
                    Qt.openUrlExternally(link)
                }
            }
        }
    }
}
