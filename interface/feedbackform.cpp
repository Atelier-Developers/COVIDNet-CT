#include <QTextStream>
#include <QFile>
#include <QDataStream>
#include <QDebug>
#include <QDir>
#include <QtSql>
#include "feedbackform.h"
#include "ui_feedbackform.h"

FeedbackForm::FeedbackForm(QWidget *parent, QString _file_path, QString _network_result) :
    QDialog(parent),
    ui(new Ui::FeedbackForm),
    file_path(_file_path),
    network_result(_network_result)
{
    ui->setupUi(this);
}

FeedbackForm::~FeedbackForm()
{
    delete ui;
}

void FeedbackForm::on_submit_button_clicked() {

    {
        // Setting up a default database connection
        QSqlDatabase db = QSqlDatabase::addDatabase("QMYSQL");
        db.setHostName("db");
        db.setDatabaseName("aphrodite_feedbacks");
        db.setUserName("aphrodite");
        db.setPassword("goddessOfLove");
        bool ok = db.open();

        if (!ok)
        {
            qDebug() << "DB NOT OPENED";
        }

        //    QFile::copy(file_path, FeedbackForm::get_feedback_path(file_path));
        //
        //    QFile file(FeedbackForm::get_feedback_path(file_path) + ".dsc");
        //   if (!file.open(QIODevice::WriteOnly | QIODevice::Text))
        //       return;

        //   QTextStream out(&file);

        // Prepare query and execute
        QSqlQuery query;
        query.prepare("INSERT INTO FEEDBACK (description, analysis, username, image_path, heatmap_path) VALUES (:description, :analysis, :username, :image_path, :heatmap_path)");
        query.bindValue(":description", ui->feedback_desc->toPlainText());
        query.bindValue(":analysis", network_result);
        query.bindValue(":username", "admin");
        query.bindValue(":image_path", file_path);
        query.bindValue(":heatmap_path", "/path/to/heatmap");
        query.exec();

        // Close database
        db.close();
    }
    //   out << "Description:\n" << ui->feedback_desc->toPlainText() << "\n" << "Network Result:\n" << network_result;

   // Closing the connection
   QSqlDatabase::removeDatabase(QSqlDatabase::defaultConnection);

   this->close();
}

QString
FeedbackForm::get_feedback_path(QString path) {
    const QFileInfo outputDir("../feedback");
    if ((!outputDir.exists()) || (!outputDir.isDir()) || (!outputDir.isWritable())) {
        qWarning() << "output directory does not exist, is not a directory, or is not writeable"
                   << outputDir.absoluteFilePath();
        QDir().mkdir("../feedback");
    }

    auto lst_slash = path.split("/");
    auto lst_backslash = lst_slash.back().split("\\");
    QString new_path = QString("../feedback/") + lst_backslash.back();
    return new_path;
}
