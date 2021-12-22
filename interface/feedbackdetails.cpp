#include "feedbackdetails.h"
#include "ui_feedbackdetails.h"

FeedbackDetails::FeedbackDetails(QWidget *parent, FeedbackData* data) :
    QDialog(parent),
    ui(new Ui::FeedbackDetails)
{
    ui->setupUi(this);

    // initial text
    ui->username_lbl->setText(data->username());
    ui->date_lbl->setText(data->date());
    ui->analysis_lbl->setText(data->analysis());
    ui->desc_lbl->setText(data->desc());

    //initial image
    QPixmap image(data->image_path());

    ui->image_lbl->setPixmap(image);
    ui->image_lbl->setScaledContents(true);
}

FeedbackDetails::~FeedbackDetails()
{
    delete ui;
}
