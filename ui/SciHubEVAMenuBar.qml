import QtQuick 2.9
import Qt.labs.platform 1.0 as Platform

Platform.MenuBar {
    Platform.Menu {
        id: menuHelp
        title: qsTr("&Edit")

        Platform.MenuItem {
            id: preferenceMenuItem
            text: qsTr("Preference")
            onTriggered: applicationWindow.showWindowPreference()
        }
    }

    Platform.Menu {
        id: menuAbout
        title: qsTr("&Help")

        Platform.MenuItem {
            id: aboutMenuItem
            text: qsTr("About")
            onTriggered: windowAbout.show()
        }
    }
}
