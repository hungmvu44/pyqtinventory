import sys
from PyQt6 import  QtWidgets
from PyQt6.QtGui import *
from PyQt6.uic import loadUi
from PyQt6.QtWidgets import *
from os import path
import sqlite3

#FORM_CLASS,_= loadUiType(path.join(path.dirname("__file__"),"main.ui"))
class MAIN(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("main.ui", self)
        self.setGeometry(200,200, 1244,966)
        self.table = self.findChild(QTableWidget, "table")
        self.search_btn = self.findChild(QPushButton, "search_btn")
        self.count_filter = self.findChild(QSpinBox, "count_lvl_filter")
        self.refresh_btn = self.findChild(QPushButton, "refresh_btn")
        self.ref_no_lbl = self.findChild(QLabel, "lbl_ref_no")
        self.parts_no_lbl = self.findChild(QLabel, "lbl_part_no")
        self.min_holes_label = self.findChild(QLabel, "lbl_min_holes")
        self.min_holes_2_label = self.findChild(QLabel, "lbl_min_holes_2")
        self.max_holes_label = self.findChild(QLabel, "lbl_max_holes")
        self.max_holes_2_label= self.findChild(QLabel, "lbl_max_holes_2")
        self.checkbtn = self.findChild(QPushButton, "check_btn")
        self.table2 = self.findChild(QTableWidget, "table_2")
        self.refresh_btn.clicked.connect(self.SHOW_parts_tb)
        self.search_btn.clicked.connect(self.SEARCH)
        self.checkbtn.clicked.connect(self.LEVEL)
        self.NAVIGATE()
        


    def SHOW_parts_tb(self):
        db = sqlite3.connect("parts.db")
        cursor = db.cursor()
        
        query = """ Select * from parts_tb """
        result = cursor.execute(query)
        
        
        self.table.setRowCount(0)
        for row_num, row_data in enumerate(result):
            self.table.insertRow(row_num)
            for col_num, data in enumerate(row_data):
                self.table.setItem(row_num, col_num, QTableWidgetItem(str(data)))

        
        #### Display references number and type number in Statistics tab
        cursor2 = db.cursor()
        cursor3 = db.cursor()

        parts_nbr = """Select COUNT (DISTINCT PartName) from parts_tb"""
        ref_nbr = """Select COUNT (DISTINCT Reference) from parts_tb"""

        result_ref_nbr = cursor2.execute(ref_nbr)
        result_parts_nbr = cursor3.execute(parts_nbr)

        self.ref_no_lbl.setText(str(result_ref_nbr.fetchone()[0]))
        self.parts_no_lbl.setText(str(result_parts_nbr.fetchone()[0]))

        #####Display results: min, max number of holes in addition to their respective references names
        cursor4 = db.cursor()
        cursor5 = db.cursor()

        min_holes_query = """Select MIN(NumberofHoles), Reference from parts_tb"""
        max_holes_query = """Select MAX(NumberofHoles), Reference from parts_tb"""

        query_min_holes = cursor4.execute(min_holes_query)
        query_max_holes = cursor5.execute(max_holes_query)
        r1 = query_min_holes.fetchone()
        r2 = query_max_holes.fetchone()
        self.min_holes_label.setText(str(r1[0]))
        self.max_holes_label.setText(str(r2[0]))
        
        self.min_holes_2_label.setText(str(r1[1]))
        self.max_holes_2_label.setText(str(r2[1]))

    def SEARCH(self):
        db = sqlite3.connect("parts.db")
        cursor = db.cursor()
        nbr = int(self.count_filter.text())
        query = f"""Select * from parts_tb WHERE Count <= {nbr}"""
        result = cursor.execute(query)
        self.table.setRowCount(0)
        for row_num, row_data in enumerate(result):
            self.table.insertRow(row_num)
            for col_num, data in enumerate(row_data):
                self.table.setItem(row_num, col_num, QTableWidgetItem(str(data)))

    def LEVEL(self):
        db = sqlite3.connect("parts.db")
        cursor = db.cursor()
        
        query = """ Select Reference,PartName,Count from parts_tb order by Count asc LIMIT 3 """
        result = cursor.execute(query)
        
        
        self.table2.setRowCount(0)
        for row_num, row_data in enumerate(result):
            self.table2.insertRow(row_num)
            for col_num, data in enumerate(row_data):
                self.table2.setItem(row_num, col_num, QTableWidgetItem(str(data)))

    def NAVIGATE(self):
        db = sqlite3.connect("parts.db")
        cursor = db.cursor()
        query = "Select * from parts_tb"

        result = cursor.execute(query)
        item = result.fetchone()

        self.ID.setText(str(item[0]))
        self.lineEdit_ref.setText(str(item[1]))
        self.lineEdit_partname.setText(str(item[2]))
        self.lineEdit_minarea.setText(str(item[3]))
        self.lineEdit_maxarea.setText(str(item[4]))
        self.lineEdit_holes.setText(str(item[5]))
        self.lineEdit_mindia.setText(str(item[6]))
        self.lineEdit_maxdia.setText(str(item[7]))
        self.count_spinbox.setValue(item[8])
    
    def UPDATE(self):
        db = sqlite3.connect('parts.db')
        cursor = db.cursor()

        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MAIN()
    win.show()
    app.exec()