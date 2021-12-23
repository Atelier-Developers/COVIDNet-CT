#include <QDateTime>
#include <QProcess>
#include "feedbackdetails.h"
#include "ui_feedbackdetails.h"

FeedbackDetails::FeedbackDetails(QWidget *parent, FeedbackData* data) :
    QDialog(parent),
    ui(new Ui::FeedbackDetails)
{
    ui->setupUi(this);

    // initial text
    ui->username_lbl->setText("User: " + data->username());
    QDateTime dateTime = QDateTime::fromString(data->date(), "yyyy-MM-ddThh:mm:ss");
    ui->date_lbl->setText("Date and Time: " + dateTime.toString("ddd MMMM yyyy, hh:mm:ss"));
    ui->analysis_lbl->setText("Model Analysis: \n\n" + data->analysis());
    ui->desc_lbl->setText("Feedback: \n\n" + data->desc());

    //initial image
    QString displayed_image_path;
    if (image_is_dicom(data))
        displayed_image_path = make_temp_image(data);
    else
        displayed_image_path = data->image_path();

    QPixmap image(displayed_image_path);

    ui->image_lbl->setPixmap(image);
    ui->image_lbl->setScaledContents(true);
}

QString
FeedbackDetails::make_temp_image(FeedbackData* data) {
    QString image_path = data->image_path();
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
    QStringList tmp_path = data->image_path().split(QString("/")).back().split(QString("."));
    return QString("../assets/temp/%1.png").arg(tmp_path[0]);
}

bool
FeedbackDetails::image_is_dicom(FeedbackData* data) {
    if(data->image_path().split(".").back().compare("dcm") == 0)
        return true;
    return false;
}

FeedbackDetails::~FeedbackDetails()
{
    delete ui;
}
