import sys

from PyQt5 import QtWidgets

from config.config_parser import ConfigParser
from database.database import DataBase
from exceptions import Exceptions
from gui.gui import AuthWindow
from utils.parser_utils import ParserUtils
from utils.secondary_utils import SecondaryUtils
from utils.security_utils import SecurityUtils


def main():
    config = ConfigParser("config/config.ini")
    parser_utils = ParserUtils(config)
    security_utils = SecurityUtils(config)
    secondary_utils = SecondaryUtils()
    exceptions = Exceptions(config)

    database = DataBase("database.sqlite3", config, parser_utils, security_utils, exceptions)

    database.delete_database()
    database.create_all_tables()

    app = QtWidgets.QApplication(sys.argv)
    window = AuthWindow(config, database, parser_utils, security_utils, secondary_utils, exceptions)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
