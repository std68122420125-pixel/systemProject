import sys
from PyQt6 import uic
from PyQt6.QtWidgets import *
from connectdb import db, cursor


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi('PcMenagement.ui', self)

        self.id = 0

        # ตั้งค่าตาราง
        self.tbPC.setColumnWidth(0, 50)
        self.tbPC.setColumnWidth(1, 150)
        self.tbPC.setColumnWidth(2, 150)
        self.tbPC.setColumnWidth(3, 100)
        self.tbPC.setColumnWidth(4, 100)

        self.tbPC.verticalHeader().setVisible(False)

        # โหลดข้อมูลทั้งหมด
        self.show_all_pcs()

        # เชื่อมปุ่ม
        self.btnadd.clicked.connect(self.insert_pc)
        self.btnclear.clicked.connect(self.clear)
        self.btnupdate.clicked.connect(self.update_pc)
        self.btndel.clicked.connect(self.delete_pc)
        self.btnSearch.clicked.connect(self.search_pc)

        # คลิกตาราง
        self.tbPC.cellClicked.connect(self.selected_row)

        # กด Enter ค้นหา
        self.txtSearch.returnPressed.connect(self.search_pc)

    def insert_pc(self):
        brand = self.txtBrand.text()
        model = self.txtModel.text()
        year = self.txtYear.text()
        price = self.txtPrice.text()

        sql = 'insert into pc(brand, model, year, price) values(?, ?, ?, ?)'
        values = (brand, model, year, price)

        rs = cursor.execute(sql, values)
        db.commit()

        if rs.rowcount > 0:
            QMessageBox.information(self, 'Information', 'เพิ่มคอมเข้าร้านสำเร็จ!')
            self.show_all_pcs()

        self.clear()

    def update_pc(self):

        if self.id == 0:
            QMessageBox.warning(self, "Warning", "กรุณาเลือกข้อมูลก่อน")
            return

        brand = self.txtBrand.text()
        model = self.txtModel.text()
        year = self.txtYear.text()
        price = self.txtPrice.text()

        sql = 'update pc set brand=?, model=?, year=?, price=? where id=?'
        values = (brand, model, year, price, self.id)

        row = cursor.execute(sql, values)
        db.commit()

        if row.rowcount > 0:
            QMessageBox.information(self, 'Information', 'อัปเดตข้อมูลสำเร็จ!')
            self.show_all_pcs()

        self.clear()

    def delete_pc(self):

        if self.id == 0:
            QMessageBox.warning(self, "Warning", "กรุณาเลือกข้อมูลก่อน")
            return

        confirm = QMessageBox.question(
            self,
            "Confirm",
            "ต้องการลบข้อมูลนี้หรือไม่?"
        )

        if confirm == QMessageBox.StandardButton.Yes:

            sql = 'delete from pc where id=?'
            values = (self.id,)

            row = cursor.execute(sql, values)
            db.commit()

            if row.rowcount > 0:
                QMessageBox.information(self, 'Information', 'ลบข้อมูลสำเร็จ!')
                self.show_all_pcs()

        self.clear()

    def selected_row(self, row, column):

        self.id = self.tbPC.item(row, 0).text()

        self.txtid.setText(self.tbPC.item(row, 0).text())
        self.txtBrand.setText(self.tbPC.item(row, 1).text())
        self.txtModel.setText(self.tbPC.item(row, 2).text())
        self.txtYear.setText(self.tbPC.item(row, 3).text())
        self.txtPrice.setText(self.tbPC.item(row, 4).text())

    def search_pc(self):

        brand = self.txtSearch.text()

        sql = 'select * from pc where brand like ?'
        values = (f'%{brand}%',)

        pcs = cursor.execute(sql, values).fetchall()

        self.show_pcs(pcs)

    def show_all_pcs(self):

        sql = 'select * from pc'
        pcs = cursor.execute(sql).fetchall()

        self.show_pcs(pcs)

    def show_pcs(self, pcs):

        self.tbPC.setRowCount(len(pcs))

        for row, s in enumerate(pcs):

            self.tbPC.setItem(row, 0, QTableWidgetItem(str(s[0])))
            self.tbPC.setItem(row, 1, QTableWidgetItem(s[1]))
            self.tbPC.setItem(row, 2, QTableWidgetItem(s[2]))
            self.tbPC.setItem(row, 3, QTableWidgetItem(str(s[3])))
            self.tbPC.setItem(row, 4, QTableWidgetItem(str(s[4])))

    def clear(self):

        self.id = 0

        self.txtid.setText('')
        self.txtBrand.setText('')
        self.txtModel.setText('')
        self.txtYear.setText('')
        self.txtPrice.setText('')

        self.tbPC.clearSelection()


if __name__ == '__main__':

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())