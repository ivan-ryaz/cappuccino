import sys
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow,QTableWidgetItem


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.db = sqlite3.connect('coffee.sqlite')
        self.setWindowTitle('Кофе')
        self.cursor = self.db.cursor()
        self.pushButton.clicked.connect(self.newCoffe)
        self.loadTable()

    def loadTable(self):
        res = self.cursor.execute('SELECT * FROM coffes').fetchall()
        self.tableWidget.setRowCount(len(res))
        self.tableWidget.setColumnCount(len(res[0]))
        self.tableWidget.setHorizontalHeaderLabels([i[0] for i in self.cursor.description])
        for i, u in enumerate(res):
            for j, k in enumerate(u):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(k)))

    def newCoffe(self):
        self.coffe = uic.loadUi('addEditCoffeeForm.ui')
        self.coffe.pushButton.clicked.connect(self.createNewCoffe)
        self.coffe.show()

    def createNewCoffe(self):
        try:
            req = f'''INSERT INTO coffes(название_сорта, степень_обжарки, вид, описание_вкуса, цена, объем_упаковки) VALUES('{
            self.coffe.lineEdit.text()}', '{self.coffe.lineEdit_2.text()}', '{self.coffe.lineEdit_3.text()}', '{self.coffe.lineEdit_4.text()}', '{
            self.coffe.lineEdit_5.text()}', '{self.coffe.lineEdit_6.text()}')'''
            print(req)
            self.cursor.execute(req)
            print(1)
            self.db.commit()
            print(2)
            self.loadTable()
        except:
            self.coffe.label_7.setText('Неверно заполнена форма')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())