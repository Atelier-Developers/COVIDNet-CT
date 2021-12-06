#include "feedbackform.h"
#include "result.h"
#include "ui_result.h"
#include "imagewindow.h"

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


void Result::on_show_heatmap_clicked() {
    QString *image_path = new QString("../assets/temp/heatmap.png");

    ImageWindow* image_window = new ImageWindow(this, image_path);

    image_window->show();
}

