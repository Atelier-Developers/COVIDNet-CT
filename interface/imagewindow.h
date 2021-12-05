#ifndef IMAGEWINDOW_H
#define IMAGEWINDOW_H

#include <QDialog>

namespace Ui {
class ImageWindow;
}

class ImageWindow : public QDialog
{
    Q_OBJECT

public:
    explicit ImageWindow(QWidget *parent = nullptr, QString *image_address = nullptr);
    ~ImageWindow();

private:
    Ui::ImageWindow *ui;
};

#endif // IMAGEWINDOW_H
