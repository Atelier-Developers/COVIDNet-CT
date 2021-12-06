#include "imagewindow.h"
#include "ui_imagewindow.h"

#include <QFileDialog>
#include <QDir>
#include <QFile>

ImageWindow::ImageWindow(QWidget *parent, QString *image_address, bool _move_able) :
    QDialog(parent),
    ui(new Ui::ImageWindow)
{
    ui->setupUi(this);

    QPixmap image(*image_address);

    ui->image_place->setPixmap(image);
    ui->image_place->setScaledContents(true);
    image_path = *image_address;

    move_able = _move_able;
    ui->save_img->setVisible(move_able);

}

ImageWindow::~ImageWindow()
{
    delete ui;
}

void ImageWindow::on_save_img_clicked()
{
    QString directory = QFileDialog::getSaveFileName(this,
                                tr("Find Files"), QDir::currentPath() + "/..");

    QFile::copy(image_path, directory);

}

