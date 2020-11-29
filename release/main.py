import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMessageBox, QWidget
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from main_ui import Ui_MainWindow
from addEditCoffeeForm_ui import Ui_MainWindow1


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.con = sqlite3.connect("../data/coffee.db")
        cur = self.con.cursor()
        # Получили результат запроса, который ввели в текстовое поле
        result = cur.execute("SELECT id, name, roast_degree, ground_beans, flavor_description, price, packing_volume "
                             "FROM coffee").fetchall()
        # Заполнили размеры таблицы
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        self.titles = [description[0] for description in cur.description]
        # Заполнили таблицу полученными элементами
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

        self.btn_add.clicked.connect(self.add_record)
        self.btn_change.clicked.connect(self.change_record)

    def add_record(self):
        self.window = EditWindowWidget(self)

        self.window.setWindowTitle("Добавлние записи")

        self.window.pushButton.clicked.connect(self.window.adding_record_db)
        self.window.table = self.tableWidget
        self.window.show()

    def change_record(self):
        self.window = EditWindowWidget(self)

        self.window.setWindowTitle("Редактирование записи")
        self.window.pushButton.setText("Сохранить")


        self.window.table = self.tableWidget
        if self.tableWidget.currentItem() is None:
            self.statusBar().showMessage('Не выбран сорт кофе')
        else:
            info_selected_record = []
            row = self.tableWidget.row(self.tableWidget.currentItem())
            for col in range(7):
                info_selected_record.append(self.tableWidget.item(row, col).text())

            self.window.line1.setText(info_selected_record[1])
            self.window.line2.setText(info_selected_record[2])
            self.window.line3.setText(info_selected_record[3])
            self.window.line4.setText(info_selected_record[4])
            self.window.line5.setText(info_selected_record[5])
            self.window.line6.setText(info_selected_record[6])

            self.window.pushButton.clicked.connect(self.window.changing_record_db)
            self.window.show()


class EditWindowWidget(QMainWindow, Ui_MainWindow1):  # Класс дополнительного окна
    def __init__(self, arg):
        super().__init__()
        self.initUI(arg)

    def initUI(self, main_window):
        self.setupUi(self)

        # Подключение db
        self.con = sqlite3.connect("../data/coffee.db")
        cur = self.con.cursor()

        self.main_window = main_window

    def update_table_widget(self):
        cur = self.main_window.con.cursor()
        # Получили результат запроса, который ввели в текстовое поле
        result = cur.execute("SELECT id, name, roast_degree, ground_beans, flavor_description, price, "
                             "packing_volume FROM coffee").fetchall()
        # Заполнили размеры таблицы
        self.table.setRowCount(len(result))
        self.table.setColumnCount(len(result[0]))
        # Заполнили таблицу полученными элементами
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.table.setItem(i, j, QTableWidgetItem(str(val)))

        self.close()

    def get_text_labels(self):
        self.cur = self.con.cursor()
        self.l1 = self.line1.text()
        self.l2 = self.line2.text()
        self.l3 = self.line3.text()
        self.l4 = self.line4.text()
        self.l5 = self.line5.text()
        self.l6 = self.line6.text()

    def checks_text_on_error(self):
        if self.l1 == "" or self.l2 == "" or self.l3 == "" or self.l4 == "" or self.l5 == "" or self.l6 == "":
            self.statusBar().showMessage('Неверно заполнена форма')
        else:
            return True

    def adding_record_db(self):
        self.get_text_labels()
        if self.checks_text_on_error() is True:
            self.cur.execute("INSERT INTO coffee(name, roast_degree, ground_beans, flavor_description, price, "
                             "packing_volume) VALUES(?, ?, ?, ?, ?, ?)",
                        (self.l1, self.l2, self.l2, self.l4, self.l5, self.l6,))
            self.con.commit()

            self.update_table_widget()

    def changing_record_db(self):
        self.get_text_labels()

        self.select_cell = self.table.currentItem()
        if self.checks_text_on_error() is True:
            info_record_which_changes = []
            info_record_which_changes.append(self.table.item(self.table.row(self.select_cell), 0).text())
            self.cur.execute("UPDATE coffee SET name = ? WHERE id = ?", (self.l1, info_record_which_changes[0],))
            self.cur.execute("UPDATE coffee SET roast_degree = ? WHERE id = ?", (self.l2, info_record_which_changes[0],))
            self.cur.execute("UPDATE coffee SET ground_beans = ? WHERE id = ?", (self.l3, info_record_which_changes[0],))
            self.cur.execute("UPDATE coffee SET flavor_description = ? "
                             "WHERE id = ?", (self.l4, info_record_which_changes[0],))
            self.cur.execute("UPDATE coffee SET price = ? WHERE id = ?", (self.l5, info_record_which_changes[0],))
            self.cur.execute("UPDATE coffee SET packing_volume = ? "
                             "WHERE id = ?", (self.l6, info_record_which_changes[0],))
            self.con.commit()

        self.update_table_widget()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())