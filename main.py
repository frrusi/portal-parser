from PyQt5 import QtWidgets

from config.config import ConfigParser
from database.database import DataBase
from gui.gui import Authorization


def main():
    import sys
    config = ConfigParser("config/config.ini")
    database = DataBase('sqlite3.sqlite3')

    database.delete_database()
    database.create_all_tables()

    app = QtWidgets.QApplication(sys.argv)
    window = Authorization(database, config)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
