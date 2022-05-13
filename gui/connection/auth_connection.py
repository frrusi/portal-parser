from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import QFileDialog
from sqlalchemy import select

from database import models
from gui.connection.journal_connection import JournalWindow
from gui.connection.main_connection import MainWindow
from gui.connection.recovery_connection import RecoveryWindow
from gui.windows import login_window
from parser.parser import Parser


class RoundPixmapStyle(QtWidgets.QProxyStyle):
    def __init__(self, radius=10, *args, **kwargs):
        super(RoundPixmapStyle, self).__init__(*args, **kwargs)
        self._radius = radius

    def drawItemPixmap(self, painter, rectangle, alignment, pixmap):
        painter.save()
        pix = QtGui.QPixmap(pixmap.size())
        pix.fill(QtCore.Qt.transparent)
        p = QtGui.QPainter(pix)
        p.setBrush(QtGui.QBrush(pixmap))
        p.setPen(QtCore.Qt.NoPen)
        p.drawRoundedRect(pixmap.rect(), self._radius, self._radius)
        p.end()
        super(RoundPixmapStyle, self).drawItemPixmap(painter, rectangle, alignment, pix)
        painter.restore()


class AuthWindow(QtWidgets.QDialog, login_window.Ui_Authorization):
    def __init__(self, config, database, exceptions, parser_utils, security_utils, secondary_utils):
        super(AuthWindow, self).__init__()

        self.config = config
        self.database = database
        self.exceptions = exceptions

        self.pt = parser_utils
        self.scrt = security_utils
        self.scnt = secondary_utils

        self.parser = Parser(database, config, exceptions, parser_utils, security_utils, secondary_utils)

        self.setupUi(self)

        self.MainWindow = MainWindow()
        self.JournalWindow = JournalWindow(database)
        self.RecoveryWindow = RecoveryWindow(config, database, exceptions, parser_utils,
                                             security_utils, secondary_utils)

        self.login.setPlaceholderText("Логин")
        self.password.setPlaceholderText("Пароль")

        self.icon.setPixmap(QtGui.QPixmap("gui/icons/logo.png"))

        self.password.setEchoMode(QtWidgets.QLineEdit.Password)

        self.entry.clicked.connect(self.auth)
        self.remember.clicked.connect(self.show_recovery_window)

        self.MainWindow.profile_menu.clicked.connect(lambda: self.change_page('profile'))
        self.MainWindow.journal_menu.clicked.connect(lambda: self.change_page('journal'))
        self.MainWindow.settings_menu.clicked.connect(lambda: self.change_page('settings'))
        self.MainWindow.help_menu.clicked.connect(lambda: self.change_page('about'))
        self.MainWindow.settings.clicked.connect(lambda: self.change_page('change'))

        self.MainWindow.image_change.clicked.connect(self.change_image_profile)
        self.MainWindow.email_change.clicked.connect(self.change_email)
        self.MainWindow.password_change.clicked.connect(self.change_password)

    def change_page(self, window):
        windows = {
            'profile': 0,
            'journal': 1,
            'change': 2,
            'settings': 3,
            'about': 4
        }

        self.MainWindow.stackedWidget.setCurrentIndex(windows[window])

    def show_recovery_window(self):
        self.parser.get_csrf()
        self.RecoveryWindow.show()

    def fill_about_user(self, information):
        self.MainWindow.name.clear()
        self.MainWindow.name.setText(f"<b>{information[0]} {information[1]}</b>")

        self.MainWindow.date.clear()
        self.MainWindow.date.setText(f"{information[3]}")

        self.MainWindow.group.clear()
        self.MainWindow.group.setText(f"{information[7]}")

        self.MainWindow.institute_about.clear()
        self.MainWindow.institute_about.setText(f"{information[4]}")

        self.MainWindow.specialization_about.clear()
        self.MainWindow.specialization_about.setText(f"{information[5]}")

        self.MainWindow.training_about.clear()
        self.MainWindow.training_about.setText(f"{information[9]}")

        self.MainWindow.profile_about.clear()
        self.MainWindow.profile_about.setText(f"{information[6]}")

        self.MainWindow.year_about.clear()
        self.MainWindow.year_about.setText(f"{information[8]}")

        self.MainWindow.email_entry.clear()
        self.MainWindow.email_entry.setText(f"{information[10]}")

    def change_image_profile(self):
        file_path = QFileDialog.getOpenFileName(self, "Выбор фотографии", "./", "Image(*.png *.jpg *.jpeg *.gif *.bmp)")[0]

        if file_path:
            self.parser.change_avatar(file_path)
            file_extension = self.scnt.get_file_extension(file_path)
            with open(file_path, "rb") as new_file, open(rf'data\user_avatar.{file_extension}', 'wb') as old_file:
                old_file.write(new_file.read())

            if file_extension == 'gif':
                path = r'data/user_avatar.gif'
                gif = QtGui.QMovie(path)
                self.MainWindow.image.setMovie(gif)
                gif.start()
            else:
                self.MainWindow.image.setPixmap(self.MainWindow.circleImage(rf'data/user_avatar.{file_extension}'))

    def change_email(self):
        email = self.MainWindow.email_entry.text()
        self.parser.change_email(email)

    def change_password(self):
        password = self.MainWindow.password_entry.text()
        self.parser.change_password(password)

        self.MainWindow.password_entry.clear()
        self.MainWindow.password_entry.setPlaceholderText('Успешно')
        pal = self.MainWindow.password_entry.palette()
        text_color = QtGui.QColor("green")

        pal.setColor(QtGui.QPalette.PlaceholderText, text_color)
        self.MainWindow.password_entry.setPalette(pal)

    def fill_combobox_group(self):
        get_all_group = self.database.get_all_groups()

        self.MainWindow.group_choice.clear()
        self.MainWindow.group_choice.addItems(['Выберите группу'] + get_all_group)

        self.MainWindow.group_choice.currentIndexChanged.connect(self.fill_combobox_semester)

    def fill_combobox_semester(self):
        self.MainWindow.semester_choice.clear()
        group = self.MainWindow.group_choice.currentText()

        group_id = self.database.get_group(group)
        if self.database.select_query(select(models.Subject).where(models.Subject.group == group_id), 2) is None:
            self.parser.get_journal(group)

        get_all_semester = self.database.get_all_semesters(group)

        self.MainWindow.semester_choice.addItems(['Выберите семестр'] + get_all_semester)

        self.MainWindow.semester_choice.currentIndexChanged.connect(self.fill_combobox_subject)

    def fill_combobox_subject(self):
        self.MainWindow.subject_choice.clear()
        group = self.MainWindow.group_choice.currentText()
        semester = self.MainWindow.semester_choice.currentText()

        get_all_subject = self.database.get_all_subjects(group, int(semester), 'text')

        self.MainWindow.subject_choice.addItems(['Выберите предмет'] + get_all_subject)

        self.MainWindow.journal_open.clicked.connect(self.fill_journal)

    def fill_journal(self):
        group = self.MainWindow.group_choice.currentText()
        semester = self.MainWindow.semester_choice.currentText()
        subject = self.MainWindow.subject_choice.currentText()

        group_id = self.database.get_group(group)
        subject_id = self.database.get_subject((models.Subject.id,), subject, semester, group)[0]
        if self.database.select_query(select(models.Marks).where(models.Marks.group == group_id,
                                                                 models.Marks.semester == int(semester),
                                                                 models.Marks.subject == subject_id), 2) is None:
            self.parser.get_marks(group, int(semester), subject)
        self.JournalWindow.initialization(group, semester, subject)

        self.JournalWindow.show()

    def auth(self):
        LOGIN = self.login.text()
        PASSWORD = self.password.text()
        CODE = self.parser.auth(LOGIN, PASSWORD)

        if CODE != self.config.successful_code:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setWindowTitle("Error")
            msg.setText(self.config.auth_error)

            msg.exec_()
        else:
            self.parser.get_user_id()
            self.parser.get_csrf()
            if self.database.select_query(select(models.Group), 2) is None:
                self.parser.get_groups()

            #self.database.synchronization_groups(self.parser.get_groups(True))

            info_about_user = self.parser.get_full_info_about_auth_user()
            self.fill_about_user(info_about_user)

            self.scnt.create_dir('data')
            url_user_avatar = self.parser.get_user_avatar()
            self.scnt.get_image(self.config.url + url_user_avatar)
            file_extension = self.scnt.get_file_extension(url_user_avatar)

            if file_extension == 'gif':
                proxy_style = RoundPixmapStyle(radius=65, style=self.MainWindow.image.style())
                self.MainWindow.image.setStyle(proxy_style)
                path = r'data/user_avatar.gif'
                gif = QtGui.QMovie(path)
                self.MainWindow.image.setMovie(gif)
                gif.start()
            else:
                self.MainWindow.image.setPixmap(self.MainWindow.circleImage(rf'data\user_avatar.{file_extension}'))

            self.fill_combobox_group()

            self.close()
            self.MainWindow.show()
