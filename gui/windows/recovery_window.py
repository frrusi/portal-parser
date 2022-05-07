# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'recovery_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_RecoveryWindow(object):
    def setupUi(self, RecoveryWindow):
        RecoveryWindow.setObjectName("RecoveryWindow")
        RecoveryWindow.resize(823, 212)
        RecoveryWindow.setStyleSheet("QWidget[objectName=\"recovery_email\"],\n"
"QWidget[objectName=\"recovery_code\"] { background-color: #f6f7fb }\n"
"\n"
"QPushButton {\n"
"    color: white;\n"
"    font-size: 12px;\n"
"    font-family: \'SESans\',Arial,sans-serif;;    \n"
"    border: 1px solid #3f5cde; \n"
"    background-color: #3f5cde;\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    border: 0px;\n"
"    background-color: #243581;    \n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    border: 0px;\n"
"    background-color: #243581; \n"
"}\n"
"\n"
"QLineEdit {\n"
"    border: 1px solid #e7e7e7;\n"
"    backgorund-color: #fbfbfb;\n"
"    border-radius: 15px;\n"
"    font-family: Montserrat Medium;\n"
"    font-size: 16px;\n"
"    padding-left: 1em;\n"
"}\n"
"")
        self.centralwidget = QtWidgets.QWidget(RecoveryWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(0, 0, 821, 211))
        self.stackedWidget.setObjectName("stackedWidget")
        self.recovery_email = QtWidgets.QWidget()
        self.recovery_email.setObjectName("recovery_email")
        self.email_subtitle = QtWidgets.QLabel(self.recovery_email)
        self.email_subtitle.setGeometry(QtCore.QRect(40, 60, 581, 21))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light")
        font.setPointSize(10)
        self.email_subtitle.setFont(font)
        self.email_subtitle.setObjectName("email_subtitle")
        self.email_title = QtWidgets.QLabel(self.recovery_email)
        self.email_title.setGeometry(QtCore.QRect(20, 10, 281, 51))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light")
        font.setPointSize(18)
        self.email_title.setFont(font)
        self.email_title.setObjectName("email_title")
        self.email_input = QtWidgets.QLineEdit(self.recovery_email)
        self.email_input.setGeometry(QtCore.QRect(180, 110, 461, 41))
        self.email_input.setStyleSheet("")
        self.email_input.setObjectName("email_input")
        self.email_apply = QtWidgets.QPushButton(self.recovery_email)
        self.email_apply.setGeometry(QtCore.QRect(350, 170, 121, 31))
        self.email_apply.setMinimumSize(QtCore.QSize(0, 0))
        self.email_apply.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.email_apply.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.email_apply.setStyleSheet("QPushButton {\n"
"    color: white;\n"
"    font-size: 12px;\n"
"    font-family: \'SESans\',Arial,sans-serif;;    \n"
"    border: 1px solid #3f5cde; \n"
"    background-color: #3f5cde;\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    border: 0px;\n"
"    background-color: #243581;    \n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    border: 0px;\n"
"    background-color: #243581; \n"
"}")
        self.email_apply.setObjectName("email_apply")
        self.stackedWidget.addWidget(self.recovery_email)
        self.recovery_code = QtWidgets.QWidget()
        self.recovery_code.setObjectName("recovery_code")
        self.code_title = QtWidgets.QLabel(self.recovery_code)
        self.code_title.setGeometry(QtCore.QRect(20, 10, 281, 51))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light")
        font.setPointSize(18)
        self.code_title.setFont(font)
        self.code_title.setObjectName("code_title")
        self.code_input = QtWidgets.QLineEdit(self.recovery_code)
        self.code_input.setGeometry(QtCore.QRect(180, 110, 461, 41))
        self.code_input.setStyleSheet("QLineEdit[objectName=\"email_system\"] {\n"
"    border: 1px solid #e7e7e7;\n"
"    backgorund-color: #fbfbfb;\n"
"    border-radius: 15px;\n"
"    font-family: Montserrat Medium;\n"
"    font-size: 16px;\n"
"    padding-left: 1em;\n"
"}\n"
"")
        self.code_input.setObjectName("code_input")
        self.code_apply = QtWidgets.QPushButton(self.recovery_code)
        self.code_apply.setGeometry(QtCore.QRect(350, 170, 121, 31))
        self.code_apply.setMinimumSize(QtCore.QSize(0, 0))
        self.code_apply.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.code_apply.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.code_apply.setStyleSheet("QPushButton {\n"
"    color: white;\n"
"    font-size: 12px;\n"
"    font-family: \'SESans\',Arial,sans-serif;;    \n"
"    border: 1px solid #3f5cde; \n"
"    background-color: #3f5cde;\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    border: 0px;\n"
"    background-color: #243581;    \n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    border: 0px;\n"
"    background-color: #243581; \n"
"}")
        self.code_apply.setObjectName("code_apply")
        self.code_subtitle = QtWidgets.QLabel(self.recovery_code)
        self.code_subtitle.setGeometry(QtCore.QRect(40, 60, 581, 21))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift Light")
        font.setPointSize(10)
        self.code_subtitle.setFont(font)
        self.code_subtitle.setObjectName("code_subtitle")
        self.stackedWidget.addWidget(self.recovery_code)
        RecoveryWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(RecoveryWindow)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(RecoveryWindow)

    def retranslateUi(self, RecoveryWindow):
        _translate = QtCore.QCoreApplication.translate
        RecoveryWindow.setWindowTitle(_translate("RecoveryWindow", "MainWindow"))
        self.email_subtitle.setText(_translate("RecoveryWindow", "Восстановление доступа возможно при наличии электронной почты в базе данных."))
        self.email_title.setText(_translate("RecoveryWindow", "Восстановление доступа"))
        self.email_input.setPlaceholderText(_translate("RecoveryWindow", "e-mail"))
        self.email_apply.setText(_translate("RecoveryWindow", "Применить"))
        self.code_title.setText(_translate("RecoveryWindow", "Восстановление доступа"))
        self.code_input.setPlaceholderText(_translate("RecoveryWindow", "Код"))
        self.code_apply.setText(_translate("RecoveryWindow", "Применить"))
        self.code_subtitle.setText(_translate("RecoveryWindow", "На почту отправлен код восстановления доступа, введите его в течение 10 минут."))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    RecoveryWindow = QtWidgets.QMainWindow()
    ui = Ui_RecoveryWindow()
    ui.setupUi(RecoveryWindow)
    RecoveryWindow.show()
    sys.exit(app.exec_())
