#ifndef FEEDBACKDETAILS_H
#define FEEDBACKDETAILS_H

#include <QDialog>

#include "feedbackdata.h"

namespace Ui {
class FeedbackDetails;
}

class FeedbackDetails : public QDialog
{
    Q_OBJECT

public:
    explicit FeedbackDetails(QWidget *parent = nullptr, FeedbackData* feedback_data = nullptr);
    ~FeedbackDetails();

private:
    Ui::FeedbackDetails *ui;
    QString make_temp_image(FeedbackData* data);
    bool image_is_dicom(FeedbackData* data);
};

#endif // FEEDBACKDETAILS_H
