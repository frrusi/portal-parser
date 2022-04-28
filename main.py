from config import ConfigParser
from database import DataBase
from gui import Authorization

from PyQt5 import QtWidgets


def main():
    import sys
    config = ConfigParser("config.ini")
    database = DataBase('sqlite3.sqlite3')

    database.delete_database()
    database.create_all_tables()

    app = QtWidgets.QApplication(sys.argv)
    window = Authorization(database, config)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
