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
    explicit ImageWindow(QWidget *parent = nullptr, QString *image_address = nullptr, bool _move_able = false, bool is_temp = false);
    ~ImageWindow();

private slots:
    void on_save_img_clicked();

private:
    Ui::ImageWindow *ui;
    QString image_path;
    bool move_able;
    bool _is_temp;
};

#endif // IMAGEWINDOW_H
