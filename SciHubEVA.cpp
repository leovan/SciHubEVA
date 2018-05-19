#include <QGuiApplication>
#include <QQuickStyle>
#include <QTranslator>
#include <QLibraryInfo>
#include <QQmlApplicationEngine>

int main(int argc, char *argv[])
{
    QCoreApplication::setAttribute(Qt::AA_EnableHighDpiScaling);
    QGuiApplication app(argc, argv);
    QQuickStyle::setStyle("Material");

    QQmlApplicationEngine engine;
    engine.load(QUrl(QStringLiteral("qrc:/ui/SciHubEVA.qml")));
    if (engine.rootObjects().isEmpty())
        return -1;

    return app.exec();
}
