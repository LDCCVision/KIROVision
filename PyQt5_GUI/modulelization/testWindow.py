from PyQt5.QtWidgets import *
from PyQt5 import QtCore

from test_codes.camera_Test import *

class Test(QWidget):
    def __init__(self,parent=None):
        super(Test, self).__init__(parent)
        self.initUI()

    def initUI(self):
        submitButton = QPushButton("&Submit")
        deleteButton = QPushButton("&Delete")

        self.inputLine = QLineEdit()
        self.inputLine.setPlaceholderText('상품번호 상품명 가격 개수 총금액')

        # submit 버튼을 누르면 이벤트 발생
        submitButton.clicked.connect(self.submitPushed)

        self.deleteIdx = QLineEdit()

        deleteButton.clicked.connect(self.deletePushed)

        MainBox = QVBoxLayout()
        InputBox = QVBoxLayout()
        ButtonBox = QHBoxLayout()

        MainBox.addLayout(InputBox)
        MainBox.addLayout(ButtonBox)

        InputBox.addWidget(self.inputLine)
        InputBox.addWidget(self.deleteIdx)
        ButtonBox.addWidget(submitButton)
        ButtonBox.addWidget(deleteButton)

        self.setLayout(MainBox)

        self.setWindowTitle('Test')
        self.setGeometry(300, 300, 300, 200)
        self.show()

    @QtCore.pyqtSlot()
    def submitPushed(self):
        itemtable = MyApp().itemtable
        row_count = itemtable.rowCount()
        itemtable.setRowCount(row_count + 1)
        text = self.inputLine.text().split()
        itemtable.setItem(row_count, 0, QTableWidgetItem(text[0]))
        itemtable.setItem(row_count, 1, QTableWidgetItem(text[1]))
        itemtable.setItem(row_count, 2, QTableWidgetItem(text[2]))
        itemtable.setItem(row_count, 3, QTableWidgetItem(text[3]))
        itemtable.setItem(row_count, 4, QTableWidgetItem(text[4]))

    @QtCore.pyqtSlot()
    def deletePushed(self):
        itemtable = MyApp().itemtable
        row_count = itemtable.rowCount()

        while True:
            state = 0
            for i in range(row_count - 1):
                if self.deleteIdx.text() == temp.text():
                    itemtable.removeRow(i)
                    state = 1
                    i = i - 1

            if state == 0: return