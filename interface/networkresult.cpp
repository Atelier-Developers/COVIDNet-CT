#include "networkresult.h"

#include <QString>
#include <QList>

NetworkResult::NetworkResult(const QString & _result)
    : result(_result){}


QString
NetworkResult::display() {
    // Normal, Pneumonia, COVID-19

    QStringList res_list = result.split(QString(" "));

    return QString("Normal:\t%1\n"
                    "Pneumonia:\t%2\n"
                    "COVID-19:\t%3").arg(res_list[0],res_list[1],res_list[2]);
}
