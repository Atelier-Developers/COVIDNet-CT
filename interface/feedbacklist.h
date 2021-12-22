#ifndef FEEDBACKLIST_H
#define FEEDBACKLIST_H

#include <QDialog>
#include <QListWidgetItem>

#include "feedbackdata.h"

namespace Ui {
class FeedbackList;
}

class FeedbackList : public QDialog
{
    Q_OBJECT

public:
    explicit FeedbackList(QWidget *parent = nullptr);
    ~FeedbackList();

private slots:
    void on_feedback_list_itemDoubleClicked(QListWidgetItem *item);

private:
    Ui::FeedbackList *ui;

    QMap<long, FeedbackData*> feedback_map;
};

#endif // FEEDBACKLIST_H
