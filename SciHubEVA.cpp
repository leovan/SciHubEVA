#include <QGuiApplication>
#include <QTranslator>
#include <QLibraryInfo>
#include <QQmlApplicationEngine>

#include <stdlib.h>

int main(int argc, char *argv[])
{
    setenv("QT_QUICK_CONTROLS_FALLBACK_STYLE", "Material", 1);
    setenv("QT_QUICK_CONTROLS_MATERIAL_THEME", "System", 1);
    setenv("QT_QUICK_CONTROLS_MATERIAL_VARIANT", "Dense", 1);
    setenv("QT_QUICK_CONTROLS_MATERIAL_ACCENT", "DeepPurple", 1);
    setenv("QT_QUICK_CONTROLS_MATERIAL_PRIMARY", "DeepPurple", 1);

    QCoreApplication::setAttribute(Qt::AA_EnableHighDpiScaling);
    QGuiApplication app(argc, argv);

    QQmlApplicationEngine engine;
    engine.load(QUrl(QStringLiteral("qrc:/ui/SciHubEVA.qml")));

    if (engine.rootObjects().isEmpty())
        return -1;

    return app.exec();
}
