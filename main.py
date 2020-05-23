
import csv
import os.path
from os import path
from PyQt5.QtWidgets import *
import pysftp 
from PyQt5.QtCore import *
import time

ssh_login="foo"
ssh_pass="foobar"
ssh_ip = "21.372.137.21"


jakusuniesztotoprzestaniedzialac = None

rows = []
headers = ["Name","Adress","Importance","Short_desc","Long_desc"]

def succes_popup(winname):
    alert = QMessageBox()
    alert.setText(winname)
    alert.exec_()

class TableModel(QAbstractTableModel):
    #global rows
    def rowCount(self, parent):
        # How many rows are there?
        return len(rows)
    def columnCount(self, parent):
        # How many columns?
        return len(headers)
    def data(self, index, role):
        if role != Qt.DisplayRole:
            return QVariant()
        # What's the value of the cell at the given index?
        return rows[index.row()][index.column()]
    def headerData(self, section, orientation, role):
        
        if role != Qt.DisplayRole or orientation != Qt.Horizontal:
            return QVariant()
        # What's the header for the given column?
        return headers[section]

def update():
    if path.exists("data.txt"):
        sftp = pysftp.Connection(ssh_ip,username=ssh_login,password=ssh_pass)
        sftp.get("data.txt")
        file = open("data.txt")
        read = csv.reader(file,delimiter=',')
        whole_file = list(read)
        wasname = False
        for ind , row in enumerate(whole_file):
            if not row:
                del whole_file[ind]
                continue
            if row[0]==f_name.text():
                wasname=True
                row[1]=f_adress.text().replace('\n','<nowalinia>')
                row[2]=f_importance.text().replace('\n','<nowalinia>')
                row[3]=f_short_desc.text().replace('\n','<nowalinia>')
                row[4]=f_long_desc.toPlainText().replace('\n','<nowalinia>')
        file.close()
        if not wasname:
            whole_file.append([])
            whole_file[-1].append(f_name.text().replace('\n','<nowalinia>'))
            whole_file[-1].append( f_adress.text().replace('\n','<nowalinia>'))
            whole_file[-1].append(f_importance.text().replace('\n','<nowalinia>'))
            whole_file[-1].append(f_short_desc.text().replace('\n','<nowalinia>'))
            whole_file[-1].append(f_long_desc.toPlainText().replace('\n','<nowalinia>'))

        whole_file.append([])
        file = open("data.txt",'w')
        writer = csv.writer(file)
        writer.writerows(whole_file)
        file.close()
        sftp.put("data.txt")
        

    else:
        file = open("data.txt",'w+')
        writer = csv.writer(file)
        writer.writerow([f_name.text(),f_adress.text(),f_importance.text(),f_short_desc.text(),f_long_desc.toPlainText().replace('\n','<nowalinia>')])
        file.close()
    succes_popup("UPADATE SUCCESSFUL")
    


def viewdb():
    global rows
    #app = QApplication([])
    sftp = pysftp.Connection(ssh_ip,username=ssh_login,password=ssh_pass)
    sftp.get("data.txt")
    file = open("data.txt")
    read = csv.reader(file,delimiter=',')
    whole_file = list(read)
    wasname = False
    print("aftpclose")
    rows = []
    rowsnum = 0
    for ind , row in enumerate(whole_file):
        if not row:
            continue
        rows.append([])
        rows[-1].append(row[0])
        rows[-1].append(row[1])
        rows[-1].append(row[2])
        rows[-1].append(row[3])
        rows[-1].append(row[4])
        rowsnum = ind
    print(rows)
    #test = QMessageBox()
    #test.exec()

    model = TableModel()

    dbwindow = QTableView()
    global jakusuniesztotoprzestaniedzialac
    jakusuniesztotoprzestaniedzialac = dbwindow
    dbwindow.setModel(model)

    print("close")
    dbwindow.show()

    
    






app = QApplication([])
window = QWidget()

box = QGroupBox()


layout = QFormLayout()
f_name = QLineEdit()
f_short_desc = QLineEdit()
f_long_desc = QTextEdit()
f_importance = QSpinBox()
f_adress = QLineEdit()
b_update = QPushButton(text="UPADTE")
b_viewdb = QPushButton(text="VIEW DB")

b_update.clicked.connect(update)
b_viewdb.clicked.connect(viewdb)

layout.addRow(QLabel("Name"),f_name)
layout.addRow(QLabel("Adress"),f_adress)
layout.addRow(QLabel("Short Desc."),f_short_desc)
layout.addRow(QLabel("Importance"),f_importance)
layout.addRow(QLabel("Long Desc."),f_long_desc)
layout.addRow(b_viewdb)
layout.addRow(b_update)


box.setLayout(layout)
window.setLayout(layout)
window.show()
app.exec()
