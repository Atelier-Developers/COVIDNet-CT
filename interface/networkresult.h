#ifndef NETWORKRESULT_H
#define NETWORKRESULT_H

#include <qstring.h>



class NetworkResult
{
private:
    QString result;
public:
    explicit NetworkResult(const QString& _result);

    QString display();
};

#endif // NETWORKRESULT_H
