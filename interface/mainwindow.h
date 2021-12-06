#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include "networkresult.h"

#include <QMainWindow>

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private slots:
    void on_image_preview_clicked();

    void on_analyze_clicked();

    void on_browser_clicked();

private:
    Ui::MainWindow *ui;

    NetworkResult* run_network();

    bool image_is_dicom();

    QString make_temp_image();
};
#endif // MAINWINDOW_H
