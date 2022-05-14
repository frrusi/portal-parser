from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem

from gui.windows import journal_window


class JournalWindow(QtWidgets.QMainWindow, journal_window.Ui_JournalWindow):
    def __init__(self, database, config):
        super(JournalWindow, self).__init__()
        self.setupUi(self)

        self.database = database
        self.config = config

    def initialization(self, group, semester, subject):
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

        self.table.setHorizontalHeaderLabels([self.config.group_list_message] + get_all_date)

        for index, value in enumerate(get_all_student):
            item = QTableWidgetItem(value)
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.table.setItem(index, 0, item)
            self.table.resizeColumnsToContents()

        for index, value in enumerate(get_all_marks):
            item = QTableWidgetItem(value)
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.table.setItem(index // len(get_all_date), index % len(get_all_date) + 1, item)
            self.table.resizeColumnsToContents()
