from PyQt5 import QtWidgets, QtGui, QtCore

from gui.windows import main_window


class MainWindow(QtWidgets.QMainWindow, main_window.Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.profile_icon.setPixmap(QtGui.QPixmap("gui/icons/navbar_profile.png"))
        self.journal_icon.setPixmap(QtGui.QPixmap("gui/icons/navbar_journal.png"))
        self.settings_icon.setPixmap(QtGui.QPixmap("gui/icons/navbar_settings.png"))
        self.help_icon.setPixmap(QtGui.QPixmap("gui/icons/navbar_help.png"))

        self.image_icon.setPixmap(QtGui.QPixmap("gui/icons/change_image.png"))
        self.email_icon.setPixmap(QtGui.QPixmap("gui/icons/change_mail.png"))
        self.password_icon.setPixmap(QtGui.QPixmap("gui/icons/change_password.png"))

        self.group_sync_icon.setPixmap(QtGui.QPixmap("gui/icons/synchronization.png"))
        self.sem_sub_sync_icon.setPixmap(QtGui.QPixmap("gui/icons/synchronization.png"))

        self.semester_icon.setPixmap(QtGui.QPixmap("gui/icons/journal_semester.png"))
        self.subject_icon.setPixmap(QtGui.QPixmap("gui/icons/journal_subject.png"))
        self.group_icon.setPixmap(QtGui.QPixmap("gui/icons/journal_group.png"))

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
