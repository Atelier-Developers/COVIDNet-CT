#include "feedbacklist.h"
#include "ui_feedbacklist.h"

#include <QListWidgetItem>
#include <QSqlDatabase>
#include <QSqlQuery>

#include "feedbackdetails.h"

FeedbackList::FeedbackList(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::FeedbackList)
{
    ui->setupUi(this);

    QSqlQuery query;
    query.exec("SELECT * FROM FEEDBACK");

    while (query.next()) {
        feedback_map[query.value(0).toInt()] = new FeedbackData(query.value(5).toString(),
                                                                query.value(1).toString(),
                                                                query.value(3).toString(),
                                                                query.value(4).toString(),
                                                                query.value(2).toString());

        QString tmp_path = query.value(5).toString().split(QString("/")).back();
        ui->feedback_list->addItem("Feedback " + query.value(0).toString() + ": On " + tmp_path + " By " + query.value(3).toString());

    }

    ui->loading->setText("");

}

FeedbackList::~FeedbackList()
{
    delete ui;
}

void FeedbackList::on_feedback_list_itemDoubleClicked(QListWidgetItem *item)
{
    QStringList tmp_list = item->text().split(' ')[1].split(':');
    FeedbackDetails *feedback_details = new FeedbackDetails(this, feedback_map[tmp_list[0].toInt()]);
    feedback_details->show();
}


