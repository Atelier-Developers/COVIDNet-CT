#ifndef FEEDBACKDATA_H
#define FEEDBACKDATA_H

#include <QString>

class FeedbackData {
public:
    FeedbackData();
    FeedbackData(QString desc,
                 QString image_path,
                 QString username,
                 QString date,
                 QString analysis);

private:
    QString _desc;
    QString _image_path;
    QString _username;
    QString _date;
    QString _analysis;

public:
    QString desc();
    QString image_path();
    QString username();
    QString date();
    QString analysis();

    QString repr();
};

#endif // FEEDBACKDATA_H
