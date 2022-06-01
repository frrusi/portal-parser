import re

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import QEvent
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileDialog
from sqlalchemy import select

from database import models
from gui.connection.journal_connection import JournalWindow
from gui.connection.main_connection import MainWindow
from gui.connection.recovery_connection import RecoveryWindow
from gui.pyqt.roundpixmapstyle import RoundPixmapStyle
from gui.windows import login_window
from parser.parser import Parser


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

        self.MainWindow = MainWindow(config)
        self.JournalWindow = JournalWindow(database, config)
        self.RecoveryWindow = RecoveryWindow(config, database, exceptions, parser_utils,
                                             security_utils, secondary_utils)

        self.icon.setPixmap(QtGui.QPixmap("gui/icons/logo.png"))
        self.visibleIcon = QIcon("gui/icons/visible_icon.svg")
        self.hiddenIcon = QIcon("gui/icons/hidden_icon.svg")

        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.toggleShowPassword = self.password.addAction(self.visibleIcon, QtWidgets.QLineEdit.TrailingPosition)
        self.toggleShowPassword.triggered.connect(self.show_password)
        self.toggleBool = False

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

        self.MainWindow.journal_open.clicked.connect(self.fill_journal)

        self.MainWindow.group_sync.clicked.connect(self.synchronization_group)
        self.MainWindow.se_gr_sync.clicked.connect(self.synchronization_subjects_and_semesters)

        self.MainWindow.help_password.installEventFilter(self)
        self.MainWindow.password_entry.textChanged.connect(self.check_password)

        self.completed_requirements = [False, False, False, False, False]

    def eventFilter(self, object, event):
        if event.type() == QEvent.Enter:
            self.MainWindow.password_help.show()
        elif event.type() == QEvent.Leave:
            self.MainWindow.password_help.hide()
        return False

    def check_password(self):
        current_password = self.MainWindow.password_entry.text()

        if len(current_password) >= 8:
            self.completed_requirements[0] = True
            self.MainWindow.size_text.setStyleSheet("color: green;")
            self.MainWindow.size_text.setText("✓ Не менее 8 символов")
        else:
            self.completed_requirements[0] = False
            self.MainWindow.size_text.setStyleSheet("color: red;")
            self.MainWindow.size_text.setText("× Не менее 8 символов")

        if len(re.sub(r'[^A-Z]+', '', current_password)) > 0:
            self.completed_requirements[1] = True
            self.MainWindow.capital_text.setStyleSheet("color: green;")
            self.MainWindow.capital_text.setText("✓ Минимум одна заглавная буква")
        else:
            self.completed_requirements[1] = False
            self.MainWindow.capital_text.setStyleSheet("color: red;")
            self.MainWindow.capital_text.setText("× Минимум одна заглавная буква")

        if len(re.sub(r'[^a-z]+', '', current_password)) > 0:
            self.completed_requirements[2] = True
            self.MainWindow.lower_text.setStyleSheet("color: green;")
            self.MainWindow.lower_text.setText("✓ Минимум одна строчная буква")
        else:
            self.completed_requirements[2] = False
            self.MainWindow.lower_text.setStyleSheet("color: red;")
            self.MainWindow.lower_text.setText("× Минимум одна строчная буква")

        if len(re.sub(r'\D+', '', current_password)) > 0:
            self.completed_requirements[3] = True
            self.MainWindow.number_text.setStyleSheet("color: green;")
            self.MainWindow.number_text.setText("✓ Минимум одна цифра")
        else:
            self.completed_requirements[3] = False
            self.MainWindow.number_text.setStyleSheet("color: red;")
            self.MainWindow.number_text.setText("× Минимум одна цифра")

        if len(re.sub(r'[^!@#$%^&*]+', '', current_password)) > 0:
            self.completed_requirements[4] = True
            self.MainWindow.special_text.setStyleSheet("color: green;")
            self.MainWindow.special_text.setText("✓ Минимум один спецсимвол")
        else:
            self.completed_requirements[4] = False
            self.MainWindow.special_text.setStyleSheet("color: red;")
            self.MainWindow.special_text.setText("× Минимум один спецсимвол")

        self.MainWindow.password_check.setValue(sum(self.completed_requirements) * 20)

        if self.MainWindow.password_check.value() == 100:
            self.MainWindow.password_check.setStyleSheet("QProgressBar::chunk:horizontal { background-color: green; }")
        elif self.MainWindow.password_check.value() > 50:
            self.MainWindow.password_check.setStyleSheet("QProgressBar::chunk:horizontal { background-color: yellow; }")
        else:
            self.MainWindow.password_check.setStyleSheet("QProgressBar::chunk:horizontal { background-color: red; }")

    def show_password(self):
        if not self.toggleBool:
            self.password.setEchoMode(QtWidgets.QLineEdit.Normal)
            self.toggleBool = True
            self.toggleShowPassword.setIcon(self.hiddenIcon)
        else:
            self.password.setEchoMode(QtWidgets.QLineEdit.Password)
            self.toggleBool = False
            self.toggleShowPassword.setIcon(self.visibleIcon)

    def synchronization_group(self):
        self.database.synchronization_groups(self.parser.get_groups(True))

    def synchronization_subjects_and_semesters(self):
        group = self.MainWindow.group_choice.currentText()
        self.parser.get_journal(group, True)

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
        file_path = QFileDialog.getOpenFileName(self, "Выбор фотографии", "./", self.config.file_extensions)[0]

        if file_path:
            self.parser.change_avatar(file_path)
            file_extension = self.scnt.get_file_extension(file_path)
            with open(file_path, "rb") as new_file, open(rf'data\user_avatar.{file_extension}', 'wb') as old_file:
                old_file.write(new_file.read())

            if file_extension == 'gif':
                self.scnt.set_and_start_gif(self.MainWindow)
            else:
                self.MainWindow.image.setPixmap(self.MainWindow.circleImage(rf'data/user_avatar.{file_extension}'))

    def change_email(self):
        email = self.MainWindow.email_entry.text()
        self.parser.change_email(email)

    def change_password(self):
        password = self.MainWindow.password_entry.text()

        if not all(self.completed_requirements):
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setWindowTitle("Ошибка")
            msg.setText("Пароль не соответствует требованиям")
            msg.exec_()
            return None

        self.parser.change_password(password)
        self.MainWindow.password_entry.clear()

    def fill_combobox_group(self):
        get_all_group = self.database.get_all_groups()

        self.MainWindow.group_choice.clear()
        self.MainWindow.group_choice.addItems([self.config.select_group_message] + get_all_group)

        self.MainWindow.group_choice.currentIndexChanged.connect(self.fill_combobox_semester)

    def fill_combobox_semester(self):
        self.MainWindow.semester_choice.clear()
        group = self.MainWindow.group_choice.currentText()

        group_id = self.database.get_group(group)
        if self.database.select_query(select(models.Subject).where(models.Subject.group == group_id), 2) is None:
            self.parser.get_journal(group)

        get_all_semester = self.database.get_all_semesters(group)

        self.MainWindow.semester_choice.addItems([self.config.select_semester_message] + get_all_semester)

        self.MainWindow.semester_choice.currentIndexChanged.connect(self.fill_combobox_subject)

    def fill_combobox_subject(self):
        self.MainWindow.subject_choice.clear()
        group = self.MainWindow.group_choice.currentText()
        semester = self.MainWindow.semester_choice.currentText()

        get_all_subject = self.database.get_all_subjects(group, int(semester), 'text')

        self.MainWindow.subject_choice.addItems([self.config.select_subject_message] + get_all_subject)

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
            msg.setWindowTitle(self.config.error_message)
            msg.setText(self.config.auth_error)

            msg.exec_()
        else:
            self.parser.get_user_id()
            self.parser.get_csrf()

            if self.database.select_query(select(models.Group), 2) is None:
                self.parser.get_groups()

            info_about_user = self.parser.get_full_info_about_auth_user()
            self.fill_about_user(info_about_user)

            self.scnt.create_dir('data')
            url_user_avatar = self.parser.get_user_avatar()
            self.scnt.get_image(self.config.url + url_user_avatar)
            file_extension = self.scnt.get_file_extension(url_user_avatar)

            if file_extension == 'gif':
                proxy_style = RoundPixmapStyle(radius=65, style=self.MainWindow.image.style())
                self.MainWindow.image.setStyle(proxy_style)
                self.scnt.set_and_start_gif(self.MainWindow)
            else:
                self.MainWindow.image.setPixmap(self.MainWindow.circleImage(rf'data\user_avatar.{file_extension}'))

            self.fill_combobox_group()

            self.close()
            self.MainWindow.show()
