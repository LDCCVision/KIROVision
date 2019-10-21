from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5 import QtGui

from test_codes.camera_Test import *

class subLayouts(QWidget):
    def __init__(self, parent=None):
        super(subLayouts, self).__init__(parent)

    def cellClicked(self, row, col):
        print("cellClicked... ", row, col)

    def set_item_table(self):
        itemtable = QTableWidget(4, 5)

        # Horizontal Header Labels 설정
        itemtable.setColumnCount(5)
        column_headers = ['상품번호', '상품명', '가격', '개수', '총 금액']
        itemtable.setHorizontalHeaderLabels(column_headers)

        # horizontalHeader Stretch
        header = itemtable.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)

        # 표를 직접 수정할 수 없다.
        itemtable.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # 셀을 클릭할 때의 이벤트를 슬롯에 연결
        itemtable.cellClicked.connect(self.cellClicked)
        # 현재 선택된 셀의 정보

        # 테이블에 임시 데이터를 넣는다.
        data = [
            ("삼성전자", "200000", 200000, "25000", "0"),
            ("셀트리온", "2100", 2100, "1500", "1"),
            ("현대차", "190000", 190000, "300000", "2"),
            ("기아차", "150000", 150000, "240000", "3")
        ]

        for idx, (hname, price_str, price, vol, num) in enumerate(data):
            itemtable.setItem(idx, 0, QTableWidgetItem(hname))

            itemtable.setItem(idx, 1, QTableWidgetItem(price_str))

            # 숫자를 기준으로 정렬하기 위함. -- default 는 '문자'임.
            item = QTableWidgetItem()
            item.setData(Qt.DisplayRole, price)
            itemtable.setItem(idx, 2, item)

            itemtable.setItem(idx, 3, QTableWidgetItem(vol))
            itemtable.setItem(idx, 4, QTableWidgetItem(num))

            return itemtable

    def update_table_layout(self):
        # global itemtable
        MyApp().itemtable.setColumnWidth(2, self.size().width() / 10)

    def load_item_layout(self):
        pixmap = QtGui.QPixmap('../item_image/item1.png')
        pixmap_resize = pixmap.scaled(self.size().width() / 16 * 9 / 2.5, self.size().width() / 16 * 9 / 2.5,
                                      QtCore.Qt.KeepAspectRatio)

        MyApp().item_Label.setPixmap(pixmap_resize)

        MyApp().item_data_layout.addWidget(MyApp().item_Label, alignment=Qt.AlignCenter)

        item_name = QLabel()
        item_name.setText("꼬깔콘")

        item_payment = QLabel()
        item_payment.setText("1500")

        MyApp().item_data_layout.addWidget(item_name)
        MyApp().item_data_layout.addWidget(item_payment)