#include <QTextStream>
#include <QFile>
#include <QDataStream>
#include "feedback_form.h"
#include "ui_feedback_form.h"

FeedbackForm::FeedbackForm(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::FeedbackForm)
{
    ui->setupUi(this);
}

FeedbackForm::~FeedbackForm()
{
    delete ui;
}
