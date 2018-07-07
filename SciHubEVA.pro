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
    ui/SciHubEVAMenuBar.qml \
    ui/SciHubEVAPreferences.qml \
    ui/SciHubEVAAddSciHubURL.qml \
    ui/SciHubEVACaptcha.qml \
    scihub_captcha.py \
    scihub_api.py
}

TRANSLATIONS += \
    translations/SciHubEVA_zh_CN.ts
