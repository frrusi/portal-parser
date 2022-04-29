from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QTableWidgetItem

from database.database import DataBase
from gui.windows import window_recovery_code, window_journal, window_login, window_recovery, window_main
from parser.parser import Parser
from utils.parser_utils import get_reset_password_message


class WindowJournal(QtWidgets.QDialog, window_journal.Ui_journal):
    def __init__(self, database, config):
        super(WindowJournal, self).__init__()
        self.setupUi(self)

        self.item = None

        self.parser = Parser(database, config)
        self.database = DataBase("sqlite3.sqlite3")

        self.setWindowTitle("Журнал успеваемости")

    def fillJournal(self, group, semester: str, subject: str):
        try:
            get_all_date = self.database.get_data(subject, semester)
            print(get_all_date)
            get_all_student = self.database.get_all_students(group, 'text')
            print(get_all_student)
            get_all_marks = self.database.get_marks(subject, semester)
            print(get_all_marks)

            self.table.setColumnCount(len(get_all_date) + 1)
            print(len(get_all_date))
            self.table.setRowCount(len(get_all_student))
            self.table.setColumnWidth(0, 200)

            for i in range(1, len(get_all_date) + 1):
                self.table.setColumnWidth(i, 50)

            self.table.setHorizontalHeaderLabels(['Список группы'] + get_all_date)

            self.table.setStyleSheet(
                'QWidget { background-color: #ffffff; } QHeaderView::section { background-color: #ffffff; }'
                'QTableWidget QTableCornerButton::section {background-color: #ffffff;}')
            self.table.setStyleSheet('selection-background-color: #ffffe0; selection-color: #000000')

            for index, value in enumerate(get_all_student):
                self.item = QTableWidgetItem(value)

                self.item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.table.setItem(index, 0, self.item)

            for index, value in enumerate(get_all_marks):
                self.item = QTableWidgetItem(value)

                self.item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                self.table.setItem(index // len(get_all_date), index % len(get_all_date) + 1, self.item)
        except Exception as ex:
            print(ex)


class WindowMain(QtWidgets.QDialog, window_main.Ui_Main):
    def __init__(self, database, config):
        super(WindowMain, self).__init__()
        self.setupUi(self)

        self.parser = Parser(database, config)

        self.image.setPixmap(self.circleImage("./icons/test.png"))
        self.image_5.setPixmap(self.circleImage("./icons/test.png"))

    @staticmethod
    def circleImage(imagePath):
        source = QtGui.QPixmap(imagePath)
        size = min(source.width(), source.height())

        target = QtGui.QPixmap(size, size)
        target.fill(QtCore.Qt.transparent)

        qp = QtGui.QPainter(target)
        qp.setRenderHints(qp.Antialiasing)
        path = QtGui.QPainterPath()
        path.addEllipse(0, 0, size, size)
        qp.setClipPath(path)

        sourceRect = QtCore.QRect(0, 0, size, size)
        sourceRect.moveCenter(source.rect().center())
        qp.drawPixmap(target.rect(), source, sourceRect)
        qp.end()

        return target


class RecoveryCode(QtWidgets.QDialog, window_recovery_code.Ui_Recovery_2):
    def __init__(self, database, config):
        super(RecoveryCode, self).__init__()
        self.setupUi(self)

        self.parser = Parser(database, config)


class RecoveryEmail(QtWidgets.QDialog, window_recovery.Ui_Recovery):
    def __init__(self, database, config):
        super(RecoveryEmail, self).__init__()
        self.response = None
        self.setupUi(self)

        self.parser = Parser(database, config)
        self.recoverCode = RecoveryCode(database, config)

        self.text_4.setText("<p>1. Если вы сотрудник, то используйте вашу корпоративную почту <b>@ut-mo.ru</b>.</p>")
        self.text_5.setText(
            "<p>2. Если вы студент и не получали логин/пароль (на руки или по почте) и не указывали <b>адрес вашей электронной почты</p>"
            "<p>в заявлении абитуриента</b>, то их (логин и пароль) можно получить в вашем деканате или по почте <i>efedotova@ut-mo.ru</i>.</p>")
        self.text_6.setText(
            "<p>3. Если вы студент и получали логин/пароль, то используйте почту, указанную при активации аккаунта</p>"
            "<p>или в заявлении абитуриента.</p>")
        self.email_system.setPlaceholderText("Ваш e-mail в системе")

        self.apply.clicked.connect(self.ShowRecoveryEmail)
        self.recoverCode.apply.clicked.connect(self.EntryRecoveryCode)

    def reset_password_email(self, email: str):
        assert self.parser.csrf is not None, 'CSRF not found'

        self.response = self.parser.session.post(self.parser.config.recovery_url, {
            'recoverystr': email, 'csrf': self.parser.csrf,
            'checkrecover': 'Применить'
        })

    def reset_password_code(self):
        code = self.recoverCode.code_email.text()

        self.parser.session.post(self.parser.config.recovery_url, {
            'recoverycode': code, 'csrf': self.parser.csrf,
            'checkcode': 'Применить'
        }, cookies=self.response.cookies)

    def ShowRecoveryEmail(self):
        try:
            self.parser.get_csrf()

            EMAIL = self.email_system.text()
            self.reset_password_email(EMAIL)

            if get_reset_password_message(self.parser.session,
                                          self.parser.config.recovery_url) == self.parser.config.enter_email_message:
                self.error.setStyleSheet('padding: 10px 10px;'
                                         'box-sizing: border-box;'
                                         'font-family: \'SESans\',Arial,sans-serif;'
                                         'font-size: 16px;'
                                         'color: #ea0e0e;')
                self.error.setAlignment(QtCore.Qt.AlignCenter)
                self.error.setText(self.parser.config.error_email_message)
            else:
                self.close()
                self.recoverCode.show()
        except Exception as ex:
            print(ex)

    def EntryRecoveryCode(self):
        try:
            self.parser.get_csrf()
            self.reset_password_code()

            if get_reset_password_message(self.parser.session,
                                          self.parser.config.recovery_url) == self.parser.config.enter_code_message:
                self.recoverCode.error.setStyleSheet('padding: 10px 10px;'
                                                     'box-sizing: border-box;'
                                                     'font-family: \'SESans\',Arial,sans-serif;'
                                                     'font-size: 16px;'
                                                     'color: #ea0e0e;')
                self.recoverCode.error.setAlignment(QtCore.Qt.AlignCenter)
                self.recoverCode.error.setText(self.parser.config.error_code_message)
            else:
                self.recoverCode.close()
        except Exception as ex:
            print(ex)


class Authorization(QtWidgets.QDialog, window_login.Ui_Authorization):
    def __init__(self, database, config):
        super(Authorization, self).__init__()
        self.setupUi(self)

        self.parser = Parser(database, config)
        self.database = DataBase("sqlite3.sqlite3")
        self.recoveryEmail = RecoveryEmail(database, config)
        self.windowMain = WindowMain(database, config)
        self.windowJournal = WindowJournal(database, config)

        self.login.setPlaceholderText("Логин")
        self.password.setPlaceholderText("Пароль")

        self.icon.setPixmap(QtGui.QPixmap("./icons/logo.png"))

        self.password.setEchoMode(QtWidgets.QLineEdit.Password)

        self.visibleIcon = QIcon("./icons/visibleicon.png")
        self.hiddenIcon = QIcon("./icons/hiddenicon.png")
        self.windowMain.semesterSelect.addItem('Нужно выбрать группу')
        self.windowMain.subjectSelect.addItem('Нужно выбрать семестр')

        self.toggleShowPassword = self.password.addAction(self.visibleIcon, QtWidgets.QLineEdit.TrailingPosition)
        self.toggleShowPassword.triggered.connect(self.textShowPassword)
        self.passwordShow = False

        self.entry.clicked.connect(self.checkAuth)
        self.remember.clicked.connect(self.recoveryShow)

        self.windowMain.apply.clicked.connect(self.emailChange)
        self.windowMain.apply_2.clicked.connect(self.passwordChange)
        self.windowMain.change.clicked.connect(self.changeImage)

    def textShowPassword(self):
        if not self.passwordShow:
            self.password.setEchoMode(QtWidgets.QLineEdit.Normal)
            self.passwordShow = True
            self.toggleShowPassword.setIcon(self.hiddenIcon)
        else:
            self.password.setEchoMode(QtWidgets.QLineEdit.Password)
            self.passwordShow = False
            self.toggleShowPassword.setIcon(self.visibleIcon)

    def recoveryShow(self):
        self.recoveryEmail.show()

    def windowMainShow(self):
        self.close()
        self.windowMain.show()

    def emailChange(self):
        email = self.windowMain.change_mail.text()
        self.parser.change_email(email)

    def passwordChange(self):
        password = self.windowMain.change_passw.text()
        self.parser.change_password(password)

    def changeImage(self):
        try:
            from tkinter import filedialog
            file_path = filedialog.askopenfilename()

            self.parser.get_user_id()
            self.parser.get_csrf()
            self.parser.change_avatar(file_path)

            self.windowMain.image.setPixmap(self.windowMain.circleImage(file_path))
            self.windowMain.image_5.setPixmap(self.windowMain.circleImage(file_path))
        except Exception as ex:
            print(ex)

    def information(self, getInfo):
        try:
            self.windowMain.fio.clear()
            self.windowMain.fio.setText(f"<strong>{getInfo[0]} {getInfo[1]} <strong>")

            self.windowMain.group.clear()
            self.windowMain.group.setText(f"Группа: <font color='#000000'>{getInfo[7]}<font></strong>")

            self.windowMain.birthday.clear()
            self.windowMain.birthday.setText(f"Дата рождения: <strong>{getInfo[3]}</strong>")

            self.windowMain.email.clear()
            self.windowMain.email.setText(f"Адрес электронной почты: <strong>{getInfo[10]}</strong>")

            self.windowMain.institute.clear()
            self.windowMain.institute.setText(f"Институт: <strong>{getInfo[4]}</strong>")

            self.windowMain.specialization.clear()
            self.windowMain.specialization.setText(f"Специальность: <strong>{getInfo[5]}</strong>")

            self.windowMain.profile_back.clear()
            self.windowMain.profile_back.setText(f"Профиль: <strong>{getInfo[6]}</strong>")

            self.windowMain.change_mail.setText(f"{getInfo[10]}")
            self.windowMain.change_passw.setPlaceholderText("Новый пароль")
        except Exception as ex:
            print(ex)

    def groupUpdate(self):
        try:
            if self.windowMain.groupSelect.currentText() == 'Выберите группу':
                self.windowMain.semesterSelect.clear()
                self.windowMain.subjectSelect.clear()

                self.windowMain.semesterSelect.addItem('Нежно выбрать группу')
                self.windowMain.subjectSelect.addItem('Нужно выбрать семестр')
            else:
                get_all_group = self.database.get_all_groups()
                print(get_all_group)

                self.windowMain.groupSelect.clear()
                self.windowMain.groupSelect.addItems(['Выберите группу'] + get_all_group)

                self.windowMain.groupSelect.currentIndexChanged.connect(self.semesterUpdate)
                self.windowMain.semesterSelect.currentIndexChanged.connect(self.subjectUpdate)
                self.windowMain.pushButton.clicked.connect(self.journalUpdate)
        except Exception as ex:
            print(ex)

    def semesterUpdate(self):
        try:
            if self.windowMain.groupSelect.currentText() == 'Выберите группу':
                self.windowMain.semesterSelect.clear()
                self.windowMain.subjectSelect.clear()

                self.windowMain.semesterSelect.addItem('Нужно выбрать группу')
                self.windowMain.subjectSelect.addItem("Нужно выбрать семестр")
            else:
                self.windowMain.semesterSelect.clear()
                self.parser.get_journal(self.windowMain.groupSelect.currentText())

                get_all_semester = self.database.get_all_semesters(self.windowMain.groupSelect.currentText())

                self.windowMain.semesterSelect.addItems(['Выберите семестр'] + get_all_semester)
        except Exception as ex:
            print(ex)

    def subjectUpdate(self):
        try:
            if self.windowMain.semesterSelect.currentText() == 'Выберите семестр':
                self.windowMain.subjectSelect.clear()
                self.windowMain.subjectSelect.addItem('Нужно выбрать семестр')
            else:
                self.windowMain.subjectSelect.clear()

                get_all_subject = self.database.get_all_subjects(self.windowMain.groupSelect.currentText(),
                                                                 self.windowMain.semesterSelect.currentText(), 'text')

                self.windowMain.subjectSelect.addItems(['Выберите предмет'] + get_all_subject)
        except Exception as ex:
            print(ex)

    def journalUpdate(self):
        try:
            group = self.windowMain.groupSelect.currentText()
            semester = self.windowMain.semesterSelect.currentText()
            subject = self.windowMain.subjectSelect.currentText()

            self.parser.get_marks(group, int(semester), subject)
            self.windowJournal.fillJournal(group, semester, subject)

            self.windowJournal.show()
        except Exception as ex:
            print(ex)

    def checkAuth(self):
        try:
            LOGIN = self.login.text()
            PASSWORD = self.password.text()
            CHECK = self.parser.auth(LOGIN, PASSWORD)

            if CHECK != 200:
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setWindowTitle("Error")
                msg.setText("Неправильный логин или пароль")

                start = msg.exec_()
            else:
                self.parser.get_user_id()
                self.parser.get_csrf()

                self.parser.get_groups()

                getInfo = self.parser.get_full_info_about_auth_user()
                self.information(getInfo)

                self.groupUpdate()

                self.windowMainShow()
        except Exception as ex:
            print(ex)
