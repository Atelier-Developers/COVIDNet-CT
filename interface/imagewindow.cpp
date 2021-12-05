#include "imagewindow.h"
#include "ui_imagewindow.h"

ImageWindow::ImageWindow(QWidget *parent, QString *image_address) :
    QDialog(parent),
    ui(new Ui::ImageWindow)
{
    ui->setupUi(this);

    QPixmap image(*image_address);

    ui->image_place->setPixmap(image);
//    ui->image_place->set

}

ImageWindow::~ImageWindow()
{
    delete ui;
}
