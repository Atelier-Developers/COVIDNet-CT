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

        ui->feedback_list->addItem(query.value(0).toString());

    }

}

FeedbackList::~FeedbackList()
{
    delete ui;
}

void FeedbackList::on_feedback_list_itemDoubleClicked(QListWidgetItem *item)
{
    FeedbackDetails *feedback_details = new FeedbackDetails(this, feedback_map[item->text().toInt()]);
    feedback_details->show();
}


