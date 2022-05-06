from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem
from sqlalchemy import select

from config.config import Config
from database import models
from gui.windows import main_window, login_window, journal_window, recovery_window
from parser.parser import Parser


class JournalWindow(QtWidgets.QMainWindow, journal_window.Ui_JournalWindow):
    def __init__(self, database):
        super(JournalWindow, self).__init__()
        self.setupUi(self)

        self.item = None

        self.database = database

    def intilization(self, group, semester, subject):
        get_all_date = self.database.get_data(subject, semester)
        get_all_student = self.database.get_all_students(group, 'text')
        get_all_marks = self.database.get_marks(subject, semester)

        self.table.setColumnCount(len(get_all_date) + 1)
        self.table.setRowCount(len(get_all_student))
        self.table.setColumnWidth(0, 200)

        for i in range(1, len(get_all_date) + 1):
            self.table.setColumnWidth(i, 50)

        self.table.horizontalHeader().setStretchLastSection(True)

        self.table.setStyleSheet(
            'QWidget { background-color: #ffffff; } QHeaderView::section { background-color: #ffffff; }'
            'QTableWidget QTableCornerButton::section {background-color: #ffffff;}')
        self.table.setStyleSheet('selection-background-color: #ffffe0; selection-color: #000000')

        self.table.setHorizontalHeaderLabels(['Список группы'] + get_all_date)

        for index, value in enumerate(get_all_student):
            self.item = QTableWidgetItem(value)

            self.item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.table.setItem(index, 0, self.item)
            self.table.resizeColumnsToContents()

        for index, value in enumerate(get_all_marks):
            self.item = QTableWidgetItem(value)

            self.item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            self.table.setItem(index // len(get_all_date), index % len(get_all_date) + 1, self.item)
            self.table.resizeColumnsToContents()


class RecoveryWindow(QtWidgets.QMainWindow, recovery_window.Ui_RecoveryWindow):
    def __init__(self, database, config, exceptions, parser_utils, security_utils, secondary_utils):
        super(RecoveryWindow, self).__init__()
        self.setupUi(self)
        self.response = None

        self.parser = Parser(database, config, exceptions, parser_utils, security_utils, secondary_utils)

        self.email_apply.clicked.connect(self.show_recovery_email)
        self.code_apply.clicked.connect(self.show_recovery_code)

    def reset_password_get_email(self, email: str):
        self.parser.exceptions.check_none(self.parser.csrf)

        self.response = self.parser.session.post(self.parser.config.recovery_url,
                                          Config.get_reset_password_data(email, self.parser.csrf))

    def reset_password_get_code(self, code: str):
        self.parser.exceptions.check_none(self.parser.csrf)

        self.parser.session.post(self.parser.config.recovery_url,
                          Config.get_recovery_code_data(code, self.parser.csrf),
                          cookies=self.response.cookies)

    def show_recovery_email(self):
        self.parser.get_csrf()

        EMAIL = self.email_input.text()

        self.reset_password_get_email(EMAIL)

        if self.parser.pt.check_reset_password_message(self.parser.pt.get_reset_password_message(self.parser.session),
                                                       self.parser.config.enter_email_message,
                                                       self.parser.config.email_error) is not None:
            self.email_input.clear()
            self.email_input.setPlaceholderText(self.parser.config.email_error)
            pal = self.email_input.palette()
            text_color = QtGui.QColor("red")

            pal.setColor(QtGui.QPalette.PlaceholderText, text_color)
            self.email_input.setPalette(pal)
        else:
            self.stackedWidget.setCurrentIndex(1)

    def show_recovery_code(self):
        self.parser.get_csrf()

        CODE = self.code_input.text()
        self.reset_password_get_code(CODE)

        if self.parser.pt.check_reset_password_message(self.parser.pt.get_reset_password_message(self.parser.session),
                                                       self.parser.config.enter_code_message,
                                                       self.parser.config.code_message_error) is not None:
            self.code_input.clear()
            self.code_input.setPlaceholderText(self.parser.config.code_message_error)
            pal = self.code_input.palette()
            text_color = QtGui.QColor("red")

            pal.setColor(QtGui.QPalette.PlaceholderText, text_color)
            self.code_input.setPalette(pal)
        else:
            self.close()


class MainWindow(QtWidgets.QMainWindow, main_window.Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.profile_icon.setPixmap(QtGui.QPixmap("gui/icons/navbar_profile.png"))
        self.journal_icon.setPixmap(QtGui.QPixmap("gui/icons/navbar_journal.png"))
        self.settings_icon.setPixmap(QtGui.QPixmap("gui/icons/navbar_settings.png"))
        self.help_icon.setPixmap(QtGui.QPixmap("gui/icons/navbar_help.png"))

        self.image_icon.setPixmap(QtGui.QPixmap("gui/icons/change_image.png"))

        self.group_icon.setPixmap(QtGui.QPixmap("gui/icons/journal_group.png"))
        self.group_sync_icon.setPixmap(QtGui.QPixmap("gui/icons/synchronization.png"))
        self.semester_icon.setPixmap(QtGui.QPixmap("gui/icons/journal_semester.png"))
        self.semester_sync_icon.setPixmap(QtGui.QPixmap("gui/icons/synchronization.png"))
        self.subject_icon.setPixmap(QtGui.QPixmap("gui/icons/journal_subject.png"))
        self.subject_sync_icon.setPixmap(QtGui.QPixmap("gui/icons/synchronization.png"))

        self.email_icon.setPixmap(QtGui.QPixmap("gui/icons/change_mail.png"))
        self.password_icon.setPixmap(QtGui.QPixmap("gui/icons/change_password.png"))

        self.db_icon.setPixmap(QtGui.QPixmap("gui/icons/sql-server.png"))

        self.developers_icon.setPixmap(QtGui.QPixmap("gui/icons/mammoth_icon.png"))

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


class AuthWindow(QtWidgets.QDialog, login_window.Ui_Authorization):
    def __init__(self, config, database, parser_utils, security_utils, secondary_utils, exceptions):
        super(AuthWindow, self).__init__()
        self.setupUi(self)

        self.config = config
        self.database = database
        self.parser_utils = parser_utils
        self.security_utils = security_utils
        self.secondary_utils = secondary_utils
        self.exceptions = exceptions

        self.parser = Parser(database, config, exceptions, parser_utils, security_utils, secondary_utils)
        self.MainWindow = MainWindow()
        self.JournalWindow = JournalWindow(database)
        self.RecoveryWindow = RecoveryWindow(database, config, exceptions, parser_utils, security_utils, secondary_utils)

        self.login.setPlaceholderText("Логин")
        self.password.setPlaceholderText("Пароль")

        self.icon.setPixmap(QtGui.QPixmap("gui/icons/logo.png"))

        self.password.setEchoMode(QtWidgets.QLineEdit.Password)

        self.entry.clicked.connect(self.auth)
        self.remember.clicked.connect(self.show_recovery_window)

        self.MainWindow.profile_menu.clicked.connect(lambda: self.change_page('profile'))
        self.MainWindow.journal_menu.clicked.connect(lambda: self.change_page('journal'))
        self.MainWindow.settings.clicked.connect(lambda: self.change_page('change'))
        self.MainWindow.settings_menu.clicked.connect(lambda: self.change_page('settings'))
        self.MainWindow.help_menu.clicked.connect(lambda: self.change_page('about'))

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
        file_path = QFileDialog.getOpenFileName(self, "Выбор фотографии", "./", "Image(*.png *.jpg *.jpeg)")[0]
        self.parser.change_avatar(file_path)

        with open(file_path, "rb") as new_file, open(r'data\user_avatar.png', 'wb') as old_file:
            old_file.write(new_file.read())

        self.MainWindow.image.setPixmap(self.MainWindow.circleImage('data/user_avatar.png'))

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
        self.JournalWindow.intilization(group, semester, subject)

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

            info_about_user = self.parser.get_full_info_about_auth_user()
            self.fill_about_user(info_about_user)

            self.secondary_utils.create_dir('data')
            url_user_avatar = self.parser.get_user_avatar()
            self.secondary_utils.get_image(self.config.url + url_user_avatar)

            self.MainWindow.image.setPixmap(self.MainWindow.circleImage('data/user_avatar.png'))

            self.fill_combobox_group()

            self.close()
            self.MainWindow.show()
