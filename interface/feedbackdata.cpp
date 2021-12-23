#include "feedbackdata.h"

FeedbackData::FeedbackData()
{
    _desc = "";
    _image_path = "";
}

FeedbackData::FeedbackData(QString desc,
                           QString image_path,
                           QString username,
                           QString date,
                           QString analysis){
    _desc = image_path;
    _image_path = desc;
    _username = username;
    _date = date;
    _analysis = analysis;
}

QString
FeedbackData::image_path() {
    return _image_path;
}

QString
FeedbackData::desc() {
    return _desc;
}

QString
FeedbackData::username() {
    return _username;
}

QString
FeedbackData::date() {
    return _date;
}

QString
FeedbackData::analysis() {
    return _analysis;
}

QString
FeedbackData::repr(){
    return desc().left(20) + "...";
}
