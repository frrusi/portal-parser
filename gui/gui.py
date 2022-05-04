from PyQt5 import QtGui, QtWidgets

from database.database import DataBase
from gui.windows import main_window, login_window, recovery_window, recovery_code_window

from parser.parser import Parser
from parser._parser_user_settings import ParserUserSettings


class MainWindow(QtWidgets.QMainWindow, main_window.Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)




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

        self.login.setPlaceholderText("Логин")
        self.password.setPlaceholderText("Пароль")

        self.icon.setPixmap(QtGui.QPixmap("gui/icons/logo.png"))

        self.password.setEchoMode(QtWidgets.QLineEdit.Password)

        self.entry.clicked.connect(self.auth)

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
            self.parser.get_groups()

            self.close()
            self.MainWindow.show()
