#include "imagewindow.h"
#include "mainwindow.h"
#include "networkresult.h"
#include "ui_mainwindow.h"
#include "result.h"
#include <iostream>

#include <QProcess>
#include <QDebug>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
}

MainWindow::~MainWindow()
{
    delete ui;
}

NetworkResult *
MainWindow::run_network(){
    QString image_path = ui->file_directory->toPlainText();
    QString heatmap_path = "heat.png";
    QString  command("./infer.sh");
    QStringList params = QStringList() << image_path << " " << heatmap_path;

    QProcess *process = new QProcess(this);
    process->start(command, params);
    process->execute(command, params);
    process->waitForFinished(-1);
    QString p_stdout(process->readAllStandardOutput());
    process->close();

    return new NetworkResult(p_stdout);
}


void MainWindow::on_image_preview_clicked() {
    QString *image_path = new QString(ui->file_directory->toPlainText());

    ImageWindow* image_window = new ImageWindow(this, image_path);

    image_window->show();
}


void MainWindow::on_analyze_clicked()
{
    NetworkResult* result = run_network();

    Result* result_window = new Result(this, result, ui->file_directory->toPlainText());
    result_window->show();
}

