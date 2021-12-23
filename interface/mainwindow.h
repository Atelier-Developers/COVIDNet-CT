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

    void on_show_feedback_clicked();

    void on_file_directory_text_change();

private:
    Ui::MainWindow *ui;

    NetworkResult* run_network();

    bool image_is_dicom();

    QString make_temp_image();

    bool initial_database();
};
#endif // MAINWINDOW_H
