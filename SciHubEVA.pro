QT += core quick quickcontrols2

CONFIG += c++11

RESOURCES += \
    SciHubEVA.qrc

lupdate_only {
SOURCES += \
    ui/*.qml \
    ui/elements/*.qml
}

TRANSLATIONS += \
    i18n/SciHubEVA_zh_CN.ts
