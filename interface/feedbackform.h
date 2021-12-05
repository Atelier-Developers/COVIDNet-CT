#ifndef FEEDBACKFORM_H
#define FEEDBACKFORM_H

#include <QDialog>

namespace Ui {
class FeedbackForm;
}

class FeedbackForm : public QDialog
{
    Q_OBJECT

public:
    explicit FeedbackForm(QWidget *parent = nullptr, QString _file_path = "", QString _network_result = "");
    ~FeedbackForm();

private slots:
    void on_submit_button_clicked();
    static QString get_feedback_path(QString path);

private:
    Ui::FeedbackForm *ui;
    QString file_path;
    QString network_result;
};

#endif // FEEDBACKFORM_H
