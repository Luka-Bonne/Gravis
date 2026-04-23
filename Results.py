import sqlite3
from PyQt5.QtWidgets import *


class ReturnResults(QMainWindow):
    def __init__(self, parent=None):
        super(ReturnResults, self).__init__(parent)
        self.con = sqlite3.connect("Stats.db")
        self.table_results()

    def table_results(self):
        cur = self.con.cursor()
        result = cur.execute("""Select * from Data""").fetchall()
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(3)

        self.titles = [description[0] for description in cur.description]

        self.tableWidget.setHorizontalHeaderItem(0, QTableWidgetItem("ID"))
        self.tableWidget.setHorizontalHeaderItem(1, QTableWidgetItem("Name"))
        self.tableWidget.setHorizontalHeaderItem(2, QTableWidgetItem("Score"))

        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.tableWidget.resize(800, 800)