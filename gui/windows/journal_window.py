# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'journal_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_journal(object):
    def setupUi(self, journal):
        journal.setObjectName("journal")
        journal.resize(1686, 672)
        journal.setStyleSheet("QWidget[objectName=\"journal\"] { background-color: white; }")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(journal)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.table = QtWidgets.QTableWidget(journal)
        self.table.setMinimumSize(QtCore.QSize(0, 0))
        self.table.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.table.setStyleSheet("QTableWidget[objectName=\"table\"] { border: 0px;}")
        self.table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.table.setObjectName("table")
        self.table.setColumnCount(0)
        self.table.setRowCount(0)
        self.verticalLayout_2.addWidget(self.table)

        self.retranslateUi(journal)
        QtCore.QMetaObject.connectSlotsByName(journal)

    def retranslateUi(self, journal):
        _translate = QtCore.QCoreApplication.translate
        journal.setWindowTitle(_translate("journal", "Form"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    journal = QtWidgets.QWidget()
    ui = Ui_journal()
    ui.setupUi(journal)
    journal.show()
    sys.exit(app.exec_())
