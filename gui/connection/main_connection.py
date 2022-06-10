from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt, QRect

from gui.windows import main_window


class MainWindow(QtWidgets.QMainWindow, main_window.Ui_MainWindow):
    def __init__(self, config):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.config = config

        self.profile_icon.setPixmap(QtGui.QPixmap(f"{config.icons_path}/navbar_profile.svg"))
        self.journal_icon.setPixmap(QtGui.QPixmap(f"{config.icons_path}/navbar_journal.svg"))
        self.settings_icon.setPixmap(QtGui.QPixmap(f"{config.icons_path}/navbar_settings.svg"))
        self.help_icon.setPixmap(QtGui.QPixmap(f"{config.icons_path}/navbar_help.svg"))

        self.image_icon.setPixmap(QtGui.QPixmap(f"{config.icons_path}/change_image.svg"))
        self.email_icon.setPixmap(QtGui.QPixmap(f"{config.icons_path}/change_mail.svg"))
        self.password_icon.setPixmap(QtGui.QPixmap(f"{config.icons_path}/change_password.svg"))

        self.group_sync_icon.setPixmap(QtGui.QPixmap(f"{config.icons_path}/synchronization.svg"))
        self.sem_gr_sync_icon.setPixmap(QtGui.QPixmap(f"{config.icons_path}/synchronization.svg"))

        self.semester_icon.setPixmap(QtGui.QPixmap(f"{config.icons_path}/journal_semester.svg"))
        self.subject_icon.setPixmap(QtGui.QPixmap(f"{config.icons_path}/journal_subject.svg"))
        self.group_icon.setPixmap(QtGui.QPixmap(f"{config.icons_path}/journal_group.svg"))

        self.db_icon.setPixmap(QtGui.QPixmap(f"{config.icons_path}/sql-server.svg"))
        self.developers_icon.setPixmap(QtGui.QPixmap(f"{config.icons_path}/mammoth_icon.svg"))

        self.help_password.setPixmap(QtGui.QPixmap(f"{config.icons_path}/question.svg"))

    @staticmethod
    def circleImage(imagePath):
        source = QtGui.QPixmap(imagePath)
        size = min(source.width(), source.height())

        target = QtGui.QPixmap(size, size)
        target.fill(Qt.transparent)

        qp = QtGui.QPainter(target)
        qp.setRenderHints(qp.Antialiasing)
        path = QtGui.QPainterPath()
        path.addEllipse(0, 0, size, size)
        qp.setClipPath(path)

        sourceRect = QRect(0, 0, size, size)
        sourceRect.moveCenter(source.rect().center())
        qp.drawPixmap(target.rect(), source, sourceRect)
        qp.end()

        return target
