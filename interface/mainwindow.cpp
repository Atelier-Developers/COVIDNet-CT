#include "imagewindow.h"
#include "mainwindow.h"
#include "networkresult.h"
#include "ui_mainwindow.h"
#include "result.h"
#include <iostream>

#include <QProcess>
#include <QDebug>
#include <QDir>
#include <QFileDialog>


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

bool
MainWindow::image_is_dicom() {
    if(ui->file_directory->toPlainText().split(".").back().compare("dcm") == 0)
        return true;
    return false;
}

QString
MainWindow::make_temp_image() {
    QString image_path = ui->file_directory->toPlainText();
    QString  command("python");
    QStringList params = QStringList() << "../read_dicom.py"
                                        << image_path
                                        << "-temp";

    QProcess *process = new QProcess(this);
    process->start(command, params);
    process->execute(command, params);
    process->waitForFinished(-1);
    QString p_stdout(process->readAllStandardOutput());
    process->close();
    QStringList tmp_path = ui->file_directory->toPlainText().split(QString("/")).back().split(QString("."));
    return QString("../assets/temp/%1.png").arg(tmp_path[0]);
}

void MainWindow::on_image_preview_clicked() {
    ui->status_lbl->setText("Loading...");
    ui->image_preview->setDisabled(true);
    ui->status_lbl->update();
    QApplication::instance()->processEvents();

    ui->status_lbl->adjustSize();
    if (image_is_dicom()){
        QString *image_path = new QString(make_temp_image());

        ImageWindow* image_window = new ImageWindow(this, image_path, true);

        image_window->show();
        ui->status_lbl->setText("");
        ui->image_preview->setEnabled(true);
        return;
    }
    QString *image_path = new QString(ui->file_directory->toPlainText());

    ImageWindow* image_window = new ImageWindow(this, image_path);

    ui->status_lbl->setText("");
    image_window->show();
}


void MainWindow::on_analyze_clicked() {
    ui->status_lbl->setText("Inferring...");
    ui->analyze->setDisabled(true);
    ui->status_lbl->update();
    QApplication::instance()->processEvents();

    NetworkResult* result = run_network();
    ui->status_lbl->setText("");
    ui->analyze->setEnabled(true);

    Result* result_window = new Result(this, result, ui->file_directory->toPlainText());
    result_window->show();
}



void MainWindow::on_browser_clicked()
{
    QString directory = QFileDialog::getOpenFileName(this,
                                tr("Find Files"), QDir::currentPath() + "/../");

    qDebug() << "DIR: " << directory;
    ui->file_directory->setText(directory);
}

