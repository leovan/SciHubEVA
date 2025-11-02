QT += core widgets quick quickcontrols2

CONFIG += c++11

RESOURCES += \
    SciHubEVA.qrc

lupdate_only {
SOURCES += \
    *.qml \
    *.py
}

TRANSLATIONS += \
    i18n/SciHubEVA_zh_CN.ts \
    i18n/SciHubEVA_pt_PT.ts
