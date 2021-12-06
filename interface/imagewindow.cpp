#include "imagewindow.h"
#include "ui_imagewindow.h"

#include <QFileDialog>
#include <QDir>
#include <QFile>

ImageWindow::ImageWindow(QWidget *parent, QString *image_address) :
    QDialog(parent),
    ui(new Ui::ImageWindow)
{
    ui->setupUi(this);

    QPixmap image(*image_address);

    ui->image_place->setPixmap(image);

}

ImageWindow::~ImageWindow()
{
    delete ui;
}

void ImageWindow::on_save_img_clicked()
{
    QString directory = QFileDialog::getSaveFileName(this,
                                tr("Find Files"), QDir::currentPath() + "/..");

    QFile::copy("../assets/heatmaps/heatmap.png", directory);

}

