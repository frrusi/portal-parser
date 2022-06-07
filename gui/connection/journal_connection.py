import pandas as pd
from PyQt5 import QtWidgets

from gui.pyqt.tablemodel import TableModel
from gui.windows import journal_window


class JournalWindow(QtWidgets.QMainWindow, journal_window.Ui_JournalWindow):
    def __init__(self, database, config):
        super(JournalWindow, self).__init__()
        self.setupUi(self)

        self.database = database
        self.config = config

    def initialization(self, group, semester, subject):
        self.table.setStyleSheet(
            'QWidget { background-color: #ffffff; } QHeaderView::section { background-color: #ffffff; }'
            'QTableView QTableCornerButton::section {background-color: #ffffff;}'
            'selection-background-color: #ffffe0; selection-color: #000000')

        get_all_date = self.database.get_data(subject, semester)
        get_all_student = self.database.get_all_students(group, 'text')
        get_all_marks = self.database.get_marks(subject, semester)

        dates_length = len(get_all_date)
        data = pd.DataFrame(
            [[full_name, *get_all_marks[index * dates_length:(index + 1) * dates_length]] for index, full_name in
             enumerate(get_all_student)], columns=[''] + get_all_date)

        model = TableModel(data)
        self.table.setModel(model)
