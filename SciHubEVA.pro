QT += core quick quickcontrols2
CONFIG += c++11

DEFINES += QT_DEPRECATED_WARNINGS

SOURCES += \
    SciHubEVA.cpp

RESOURCES += \
    SciHubEVA.qrc

lupdate_only {
SOURCES += \
    ui/SciHubEVA.qml \
    ui/SciHubEVAAbout.qml \
    ui/SciHubEVAAddSciHubURL.qml \
    ui/SciHubEVACaptcha.qml \
    ui/SciHubEVAMenuBar.qml \
    ui/SciHubEVAMessage.qml \
    ui/SciHubEVAPreferences.qml
}

TRANSLATIONS += \
    translations/SciHubEVA_zh_CN.ts
