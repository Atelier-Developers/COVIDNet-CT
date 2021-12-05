#ifndef IMAGE_H
#define IMAGE_H

#include <QDialog>

namespace Ui {
class Image;
}

class Image : public QDialog
{
    Q_OBJECT

public:
    explicit Image(QWidget *parent = nullptr, QString image_address = "");
    ~Image();

private:
    Ui::Image *ui;
    QString image_address;
};

#endif // IMAGE_H
