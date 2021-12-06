#ifndef RESULT_H
#define RESULT_H

#include "networkresult.h"

#include <QDialog>

namespace Ui {
class Result;
}

class Result : public QDialog
{
    Q_OBJECT

public:
    explicit Result(QWidget *parent = nullptr, NetworkResult* _network_result = nullptr, QString _file_path = "");
    ~Result();

private slots:
    void on_feedback_button_clicked();

    void on_show_heatmap_clicked();

private:
    Ui::Result *ui;
    NetworkResult* network_result;
    QString file_path;
};

#endif // RESULT_H
