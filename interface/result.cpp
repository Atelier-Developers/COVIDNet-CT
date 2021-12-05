#include "feedbackform.h"
#include "result.h"
#include "ui_result.h"

Result::Result(QWidget *parent, NetworkResult* _network_result, QString _file_path) :
    QDialog(parent),
    ui(new Ui::Result),
    file_path(_file_path)
{
    ui->setupUi(this);
    network_result = _network_result;

    ui->result->setText(network_result->display());
}

Result::~Result()
{
    delete ui;
}

void Result::on_feedback_button_clicked() {
    FeedbackForm * form = new FeedbackForm(this, file_path, network_result->display());
    form->show();
}

