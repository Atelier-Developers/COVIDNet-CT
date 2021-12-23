#include <QDateTime>
#include "feedbackdetails.h"
#include "ui_feedbackdetails.h"

FeedbackDetails::FeedbackDetails(QWidget *parent, FeedbackData* data) :
    QDialog(parent),
    ui(new Ui::FeedbackDetails)
{
    ui->setupUi(this);

    // initial text
    ui->username_lbl->setText("User: " + data->username());
    QDateTime dateTime = QDateTime::fromString(data->date(), "yyyy-MM-ddThh:mm:ss");
    ui->date_lbl->setText("Date and Time: " + dateTime.toString("ddd MMMM yyyy, hh:mm:ss"));
    ui->analysis_lbl->setText("Model Analysis: \n\n" + data->analysis());
    ui->desc_lbl->setText("Feedback: \n\n" + data->desc());

    //initial image
    QPixmap image(data->image_path());

    ui->image_lbl->setPixmap(image);
    ui->image_lbl->setScaledContents(true);
}

FeedbackDetails::~FeedbackDetails()
{
    delete ui;
}
