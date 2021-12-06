#include "networkresult.h"
#include <QDebug>

#include <QString>
#include <QList>

NetworkResult::NetworkResult(const QString & _result)
    : result(_result){}


QString
NetworkResult::display() {
    // Normal, Pneumonia, COVID-19

    QStringList res_list = result.split(QString("\n")).back().split(QString(" "));
    qDebug() << "LST1: " << result.split(QString("\n")).back();
    qDebug() << "LST2: " << result.split(QString("\n")).back().split(QString(" "));
    return QString("Predicted Class: %1\n"
                    "Normal: %2\n"
                    "Pneumonia: %3\n"
                    "COVID-19: %4").arg(res_list[0], res_list[1], res_list[2], res_list[3]);
}
