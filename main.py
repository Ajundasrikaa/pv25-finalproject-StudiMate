import sys
import sqlite3
import csv
from fpdf import FPDF
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class InsertDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(InsertDialog, self).__init__(*args, **kwargs)
        self.setWindowTitle("Add Student")
        self.setFixedSize(300, 250)

        self.QBtn = QPushButton("Register")
        self.QBtn.clicked.connect(self.addstudent)

        layout = QVBoxLayout()
        self.nameinput = QLineEdit()
        self.nameinput.setPlaceholderText("Name")
        layout.addWidget(self.nameinput)

        self.branchinput = QComboBox()
        self.branchinput.addItems(["Mechanical", "Civil", "Electrical", "Electronics and Communication", "Computer Science", "Information Technology"])
        layout.addWidget(self.branchinput)

        self.seminput = QComboBox()
        self.seminput.addItems([str(i) for i in range(1, 9)])
        layout.addWidget(self.seminput)

        self.mobileinput = QLineEdit()
        self.mobileinput.setPlaceholderText("Mobile")
        self.mobileinput.setInputMask('99999 99999')
        layout.addWidget(self.mobileinput)

        self.addressinput = QLineEdit()
        self.addressinput.setPlaceholderText("Address")
        layout.addWidget(self.addressinput)

        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def addstudent(self):
        name = self.nameinput.text()
        branch = self.branchinput.currentText()
        sem = self.seminput.currentText()
        mobile = self.mobileinput.text()
        address = self.addressinput.text()
        try:
            conn = sqlite3.connect("database.db")
            c = conn.cursor()
            c.execute("INSERT INTO students (name,branch,sem,mobile,address) VALUES (?,?,?,?,?)", (name, branch, sem, mobile, address))
            conn.commit()
            conn.close()
            QMessageBox.information(self, 'Success', 'Student added successfully!')
            self.close()
        except Exception as e:
            QMessageBox.warning(self, 'Error', str(e))

class UpdateDialog(QDialog):
    def __init__(self, student_id, *args, **kwargs):
        super(UpdateDialog, self).__init__(*args, **kwargs)
        self.setWindowTitle("Update Student")
        self.setFixedSize(300, 250)
        self.student_id = student_id

        self.QBtn = QPushButton("Update")
        self.QBtn.clicked.connect(self.updatestudent)

        layout = QVBoxLayout()
        self.nameinput = QLineEdit()
        layout.addWidget(self.nameinput)

        self.branchinput = QComboBox()
        self.branchinput.addItems(["Mechanical", "Civil", "Electrical", "Electronics and Communication", "Computer Science", "Information Technology"])
        layout.addWidget(self.branchinput)

        self.seminput = QComboBox()
        self.seminput.addItems([str(i) for i in range(1, 9)])
        layout.addWidget(self.seminput)

        self.mobileinput = QLineEdit()
        self.mobileinput.setInputMask('9999 9999 99999')
        layout.addWidget(self.mobileinput)

        self.addressinput = QLineEdit()
        layout.addWidget(self.addressinput)

        layout.addWidget(self.QBtn)
        self.setLayout(layout)

        self.populate_fields()

    def populate_fields(self):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("SELECT * FROM students WHERE roll=?", (self.student_id,))
        student = c.fetchone()
        conn.close()

        self.nameinput.setText(student[1])
        self.branchinput.setCurrentText(student[2])
        self.seminput.setCurrentText(str(student[3]))
        self.mobileinput.setText(str(student[4]))
        self.addressinput.setText(student[5])

    def updatestudent(self):
        name = self.nameinput.text()
        branch = self.branchinput.currentText()
        sem = self.seminput.currentText()
        mobile = self.mobileinput.text()
        address = self.addressinput.text()

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("UPDATE students SET name=?, branch=?, sem=?, mobile=?, address=? WHERE roll=?",
                  (name, branch, sem, mobile, address, self.student_id))
        conn.commit()
        conn.close()
        QMessageBox.information(self, 'Updated', 'Student updated successfully!')
        self.close()

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setFixedSize(350, 200)
        self.setWindowTitle("Login - StudiMate")
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f0f5;
                font-family: Arial;
            }
            QLabel#titleLabel {
                font-size: 20px;
                font-weight: bold;
                color: #2c3e50;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 8px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)

        layout = QVBoxLayout()

        # Title label
        title = QLabel("Login to StudiMate")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Password field
        self.passinput = QLineEdit()
        self.passinput.setEchoMode(QLineEdit.Password)
        self.passinput.setPlaceholderText("Enter Password")
        layout.addWidget(self.passinput)

        # Login button
        self.QBtn = QPushButton("Login")
        self.QBtn.clicked.connect(self.login)
        layout.addWidget(self.QBtn)

        self.setLayout(layout)

    def login(self):
        if self.passinput.text() == "123456":
            self.accept()
        else:
            QMessageBox.warning(self, 'Error', 'Wrong Password')

class AboutDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 200)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("STDMGMT"))
        layout.addWidget(QLabel("Version 1.0"))
        layout.addWidget(QLabel("Created by Ajundasrika Anugrahanti TS (F1D022108)"))
        btn_box = QDialogButtonBox(QDialogButtonBox.Ok)
        btn_box.accepted.connect(self.accept)
        layout.addWidget(btn_box)
        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("StudiMate")
        self.resize(800, 600)

        self.conn = sqlite3.connect("database.db")
        self.c = self.conn.cursor()
        self.c.execute("""CREATE TABLE IF NOT EXISTS students(
            roll INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT, branch TEXT, sem INTEGER,
            mobile TEXT, address TEXT)""")
        self.conn.commit()
        self.conn.close()

        # Table
        self.tableWidget = QTableWidget()
        self.setCentralWidget(self.tableWidget)
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(["Roll No", "Name", "Branch", "Sem", "Mobile", "Address", "Action"])
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Menu Bar
        menu = self.menuBar()
        file_menu = menu.addMenu("File")
        file_menu.addAction("Export to CSV", self.exportToCSV)
        file_menu.addAction("Export to PDF", self.exportToPDF)
        file_menu.addSeparator()
        file_menu.addAction("Insert Student", self.insert)
        file_menu.addSeparator()
        file_menu.addAction("Exit", self.close)

        help_menu = menu.addMenu("Help")
        help_menu.addAction("About", self.about)

        # Toolbar
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        toolbar.addAction("Add", self.insert)
        toolbar.addAction("Refresh", self.loaddata)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by name or roll no.")
        toolbar.addWidget(self.search_input)

        btn_search = QPushButton("Search")
        btn_search.clicked.connect(self.searchstudent)
        toolbar.addWidget(btn_search)

        btn_clear = QPushButton("Clear Search")
        btn_clear.clicked.connect(self.loaddata)
        toolbar.addWidget(btn_clear)

        # Status Bar
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        self.statusbar.showMessage("Ajundasrika Anugrahanti TS - F1D022108")
        

        self.setStyleSheet("""
            QMainWindow { background: #f5f6fa; }
            QTableWidget { background: white; font-size: 12px; }
            QPushButton { background-color: #2ecc71; color: white; border-radius: 4px; padding: 5px; }
            QPushButton:hover { background-color: #27ae60; }
            QStatusBar { background: #dcdde1; font-style: italic; }
        """)

        self.loaddata()

    def insert(self):
        dlg = InsertDialog()
        dlg.exec_()
        self.loaddata()

    def about(self):
        dlg = AboutDialog()
        dlg.exec_()

    def loaddata(self):
        self.tableWidget.setRowCount(0)
        conn = sqlite3.connect("database.db")
        result = conn.execute("SELECT * FROM students")
        for row_num, row_data in enumerate(result):
            self.tableWidget.insertRow(row_num)
            for col_num, data in enumerate(row_data):
                self.tableWidget.setItem(row_num, col_num, QTableWidgetItem(str(data)))
            self.addActionButtons(row_num, row_data[0])
        conn.close()

    def addActionButtons(self, row, student_id):
        btn_edit = QPushButton("Edit")
        btn_edit.setStyleSheet("""
            QPushButton {
            background-color: #27ae60;
            color: white;
            padding: 5px;
            border-radius: 4px;
            font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
        """)
        btn_edit.clicked.connect(lambda: self.editstudent(student_id))

        btn_delete = QPushButton("Hapus")
        btn_delete.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                padding: 5px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        btn_delete.clicked.connect(lambda: self.deletestudent(student_id))

        layout = QHBoxLayout()
        layout.addWidget(btn_edit)
        layout.addWidget(btn_delete)
        layout.setContentsMargins(0, 0, 0, 0)  
        layout.setSpacing(5)

        widget = QWidget()
        widget.setLayout(layout)
        self.tableWidget.setCellWidget(row, 6, widget)

    def editstudent(self, student_id):
        dlg = UpdateDialog(student_id)
        dlg.exec_()
        self.loaddata()

    def deletestudent(self, student_id):
        confirm = QMessageBox.question(self, "Confirm", "Delete this student?", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            conn = sqlite3.connect("database.db")
            conn.execute("DELETE FROM students WHERE roll=?", (student_id,))
            conn.commit()
            conn.close()
            self.loaddata()

    def searchstudent(self):
        keyword = self.search_input.text()
        conn = sqlite3.connect("database.db")
        result = conn.execute("SELECT * FROM students WHERE name LIKE ? OR roll LIKE ?", (f"%{keyword}%", f"%{keyword}%"))
        self.tableWidget.setRowCount(0)
        for row_num, row_data in enumerate(result):
            self.tableWidget.insertRow(row_num)
            for col_num, data in enumerate(row_data):
                self.tableWidget.setItem(row_num, col_num, QTableWidgetItem(str(data)))
            self.addActionButtons(row_num, row_data[0])
        conn.close()

    def exportToCSV(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save CSV", "", "CSV Files (*.csv)")
        if path:
            with open(path, 'w', newline='') as file:
                writer = csv.writer(file)
                headers = [self.tableWidget.horizontalHeaderItem(i).text() for i in range(6)]
                writer.writerow(headers)
                for row in range(self.tableWidget.rowCount()):
                    row_data = [self.tableWidget.item(row, col).text() if self.tableWidget.item(row, col) else '' for col in range(6)]
                    writer.writerow(row_data)

    def exportToPDF(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save PDF", "", "PDF Files (*.pdf)")
        if path:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=10)
            headers = [self.tableWidget.horizontalHeaderItem(i).text() for i in range(6)]
            col_width = 190 / len(headers)
            for header in headers:
                pdf.cell(col_width, 10, header, border=1)
            pdf.ln()
            for row in range(self.tableWidget.rowCount()):
                for col in range(6):
                    text = self.tableWidget.item(row, col).text() if self.tableWidget.item(row, col) else ""
                    pdf.cell(col_width, 10, text, border=1)
                pdf.ln()
            pdf.output(path)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login = LoginDialog()
    if login.exec_() == QDialog.Accepted:
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())