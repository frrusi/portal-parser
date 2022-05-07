from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QTableWidgetItem

from gui.windows import journal_window


class JournalWindow(QtWidgets.QMainWindow, journal_window.Ui_JournalWindow):
    def __init__(self, database):
        super(JournalWindow, self).__init__()
        self.setupUi(self)

        self.database = database
        self.item = None

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
