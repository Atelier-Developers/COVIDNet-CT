#include <QTextStream>
#include <QFile>
#include <QDataStream>
#include <QFile>
#include "feedbackform.h"
#include "ui_feedbackform.h"

FeedbackForm::FeedbackForm(QWidget *parent, QString _file_path, QString _network_result) :
    QDialog(parent),
    ui(new Ui::FeedbackForm),
    file_path(_file_path),
    network_result(_network_result)
{
    ui->setupUi(this);
}

FeedbackForm::~FeedbackForm()
{
    delete ui;
}

void FeedbackForm::on_submit_button_clicked() {
    /*QFile::copy(file_path, FeedbackForm::get_feedback_path(file_path));

    QFile file(FeedbackForm::get_feedback_path(file_path) + ".dsc");
   if (!file.open(QIODevice::WriteOnly | QIODevice::Text))
       return;

   QTextStream out(&file);
   out << "Description:\n" << ui->feedback_desc->toPlainText() << "\n" << "Network Result:\n" << network_result;
   this->close();*/
}

QString
FeedbackForm::get_feedback_path(QString path) {
    auto lst_slash = path.split("/");
    auto lst_backslash = lst_slash.back().split("\\");
    QString new_path = QString("F:\\pp\\qt\\feedback\\") + lst_backslash.back();
    return new_path;
}
