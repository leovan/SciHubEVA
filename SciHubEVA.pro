QT += core quick quickcontrols2
CONFIG += c++11

RESOURCES += \
    SciHubEVA.qrc

lupdate_only {
SOURCES += \
    ui/About.qml \
    ui/AddSciHubURL.qml \
    ui/App.qml \
    ui/Captcha.qml \
    ui/Message.qml \
    ui/Preferences.qml
}

TRANSLATIONS += \
    translations/SciHubEVA_zh_CN.ts
