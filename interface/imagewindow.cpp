#include "imagewindow.h"
#include "ui_imagewindow.h"

#include <QFileDialog>
#include <QDir>
#include <QFile>
#include <QDebug>

ImageWindow::ImageWindow(QWidget *parent, QString *image_address, bool _move_able, bool is_temp) :
    QDialog(parent),
    ui(new Ui::ImageWindow)
{
    ui->setupUi(this);

    QPixmap image(*image_address);

    ui->image_place->setPixmap(image);
    ui->image_place->setScaledContents(true);
    image_path = *image_address;

    move_able = _move_able;
    _is_temp = is_temp;
    ui->save_img->setVisible(move_able);

}

ImageWindow::~ImageWindow()
{
    delete ui;
    qDebug() << "DELETEING:" << image_path;
    if (QFile::exists(image_path) && _is_temp)
        QFile::remove(image_path);
}

void ImageWindow::on_save_img_clicked()
{
    QString directory = QFileDialog::getSaveFileName(this,
                                tr("Find Files"), QDir::currentPath() + "/..");

    QFile::rename(image_path, directory);

}

