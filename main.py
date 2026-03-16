import sys
from PyQt6 import uic
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from connectdb import db, cursor

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # ดึงไฟล์ UI ร้านคอมมึงมาใช้ (อิงตามชื่อที่โชว์ในจอมึงนะ)
        uic.loadUi('PcMenagement.ui', self)
        self.id = 0

        # จัดความกว้างตาราง 5 ช่อง
        self.tbPc.setColumnWidth(0, 50)
        self.tbPc.setColumnWidth(1, 150)
        self.tbPc.setColumnWidth(2, 150)
        self.tbPc.setColumnWidth(3, 100)
        self.tbPc.setColumnWidth(4, 100)
        
        # ซ่อนเลขบรรทัดที่แถมมาให้ตารางดูคลีนๆ
        self.tbPC.verticalHeader().setVisible(False)

        self.show_all_pcs()
        
        self.btnAdd.clicked.connect(self.insert_pc)
        self.btnSearch.clicked.connect(self.search_pc)
        self.btnClear.clicked.connect(self.clear)
        self.btnUpdate.clicked.connect(self.update_pc)
        self.btnDelete.clicked.connect(self.delete_pc)
        self.tbPC.cellClicked.connect(self.selected_row)

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
        # ดูดข้อมูลใหม่มาให้หมดทุกช่อง เพราะเราไม่ได้ล็อคอะไรแล้ว!
        brand = self.txtBrand.text()
        model = self.txtModel.text()
        year = self.txtYear.text()
        price = self.txtPrice.text()
        
        # อัปเดตมันทุกอย่างเลย
        sql = 'update pc set brand = ?, model = ?, year = ?, price = ? where id = ?'
        values = (brand, model, year, price, self.id)

        row = cursor.execute(sql, values)
        db.commit()

        if row.rowcount > 0:
            QMessageBox.information(self, 'Information', 'อัปเดตข้อมูลคอมสำเร็จ!')
            self.show_all_pcs()
        self.clear()

    def delete_pc(self):
        sql = 'delete from pc where id = ?'
        values = (self.id, )

        row = cursor.execute(sql, values)
        db.commit()

        if row.rowcount > 0:
            QMessageBox.information(self, 'Information', 'ลบข้อมูลคอมทิ้งแล้ว!')
            self.show_all_pcs()
        self.clear()

    def selected_row(self):
        row = self.tbPC.currentRow()
        
        # ดึงข้อมูลมาโชว์ในช่องกรอก
        self.id = self.tbPC.item(row, 0).text()
        self.txtid.setText(self.tbPC.item(row, 0).text())
        self.txtBrand.setText(self.tbPC.item(row, 1).text())
        self.txtModel.setText(self.tbPC.item(row, 2).text())
        self.txtYear.setText(self.tbPC.item(row, 3).text())
        self.txtPrice.setText(self.tbPC.item(row, 4).text())

        # *** ตามสั่งคาสะ: ไม่มีการใส่ setEnabled(False) ล็อคช่องใดๆ ทั้งสิ้น! พิมพ์แก้ได้ตามสบาย! ***

    def search_pc(self):
        brand = self.txtSearch.text()
        sql = 'select * from pc where brand like ?'
        values = (f'%{brand}%', )
        pcs = cursor.execute(sql, values).fetchall()
        self.show_pcs(pcs)
        self.txtSearch.setText('')

    def show_all_pcs(self):
        sql = 'select * from pc'
        pcs = cursor.execute(sql).fetchall()
        self.show_pcs(pcs)

    def show_pcs(self, pcs):
        n = len(pcs)
        self.tbPC.setRowCount(n)
        row = 0
        for s in pcs:
            self.tbPC.setItem(row, 0, QTableWidgetItem(str(s[0])))
            self.tbPC.setItem(row, 1, QTableWidgetItem(s[1]))
            self.tbPC.setItem(row, 2, QTableWidgetItem(s[2]))
            self.tbPC.setItem(row, 3, QTableWidgetItem(str(s[3])))
            self.tbPC.setItem(row, 4, QTableWidgetItem(str(s[4])))
            row += 1

    def clear(self):
        self.txtid.setText('')
        self.txtBrand.setText('')
        self.txtModel.setText('')
        self.txtYear.setText('')
        self.txtPrice.setText('')
        
        self.tbPC.clearSelection()
        self.show_all_pcs()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


