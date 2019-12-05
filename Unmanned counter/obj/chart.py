from PyQt5.QtWidgets import QWidget, QTableWidget, QHeaderView, QAbstractItemView, QTableWidgetItem, QVBoxLayout
from PyQt5.Qt import *

import sys

column_headers = ['상품번호', '상품명', '가격', '개수', '총 금액']

data = [
            ("삼성전자", "200000", 200000, "25000", "0"),
            ("셀트리온", "2100", 2100, "1500", "1"),
            ("현대차", "190000", 190000, "300000", "2"),
            ("기아차", "150000", 150000, "240000", "3")
        ]

merchant_dictionary = {'class_id': [x for x in range(51)],
                       'name': ['데미소다 (자몽)(250ml)', '펩시콜라 (1.5L)', '태양의 식후비법W (500ml)', '아침에사과 (500ml)', '펩시콜라캔 (250ml)',
                                '썬키스트 레몬에이드 (350ml)', '코카콜라 제로 (250ml)', '구구콘', '부라보콘 바닐라', '월드콘 바닐라',
                                '폴라포 포도', '월드콘 초코', '환타 (오렌지)(1.5L)', '진라면 큰컵 순한맛', '진라면 큰컵 매운맛',
                                '초코파이 바나나', '칙촉 오리지널', '리츠 크래커', '해장의 신 속풀라면', '감동의 신 속찬라면',
                                '미니컵면 가쓰오우동맛', '미니컵면 시원한 해장국맛', '오징어 짬뽕 작은 컵', '제주감귤 (1.5L)', '너구리 작은 컵',
                                '칙촉 티라미수', '리츠샌드 레몬', '리츠샌드 치즈', '신라면 블랙 봉지', '감자면 봉지',
                                '사천 짜파게티', '짜파게티', '신라면 봉지', '바나나킥', '칠성사이다 (1.5L)',
                                '양파링', '꽃개랑', '구운 양파', '포카칩 어니언', '신라면 작은 컵',
                                '고통의 신 속타는라면', '딸기에몽 (180ml)', '매일두유 99.89 (190ml)', '초코에몽 (180ml)', '허쉬초코드링크 (190ml)',
                                '코카콜라 (1.5L)', '피크닉 사과 (200ml)', '씨그램 (레몬)(350ml)', '트레비 (라임)(500ml)', '데미소다 (애플)(250ml)',
                                '밀키스 (250ml)'],
                       'price': ['1200', '2800', '1800', '1700', '1200',
                                 '1500', '1400', '1800', '1800', '1800',
                                 '1200', '1800', '2800', '950', '950',
                                 '4800', '2400', '1500', '1500', '1500',
                                 '700', '700', '900', '1900', '950',
                                 '2400', '1900', '1900', '1600', '1200',
                                 '1150', '950', '850', '1500', '3200',
                                 '1500', '1500', '1500', '1500', '900',
                                 '1500', '1000', '1000', '1000', '1000',
                                 '3400', '500', '1300', '1600', '1200',
                                 '1200']}

class tableMaker(QWidget):

    id_signal = pyqtSignal(str)
    price_signal = pyqtSignal(str)
    name_signal = pyqtSignal(str)
    show_change = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.class_list = []

    def setTable(self):
        # 아이템 차트의 초기값 4열 5행
        # 표안의 값은 수정 불가능
        # 각 속성의 공간은 표 전체를 균일하게 나누어 갖는다 남는 공간은 없다.\

        global class_list

        self.table = QTableWidget(0, 5)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setColumnCount(5)

        global column_headers
        self.table.setHorizontalHeaderLabels(column_headers)

        self.header = self.table.horizontalHeader()
        self.header.setSectionResizeMode(0, QHeaderView.Stretch)
        self.header.setSectionResizeMode(1, QHeaderView.Stretch)
        self.header.setSectionResizeMode(2, QHeaderView.Stretch)
        self.header.setSectionResizeMode(3, QHeaderView.Stretch)
        self.header.setSectionResizeMode(4, QHeaderView.Stretch)

        # 셀에 내용을 띄워주기 위한 임시적인 데이터
        global data
        global merchant_dictionary

        for idx, (num, name, price, count, sum_price) in enumerate(data):
            self.table.setItem(idx, 0, QTableWidgetItem(num))

            self.table.setItem(idx, 1, QTableWidgetItem(name))

            # 숫자를 기준으로 정렬하기 위함. -- default 는 '문자'임.
            self.item = QTableWidgetItem()
            self.item.setData(Qt.DisplayRole, price)
            self.table.setItem(idx, 2, self.item)

            self.table.setItem(idx, 3, QTableWidgetItem(count))
            self.table.setItem(idx, 4, QTableWidgetItem(sum_price))

        # 이미지에서 전송받은 클래스를 이용하여 표를 초기화 해주는 부분
        # 리스트에서 중복을 제거한 리스트를 따로 저장

        self.table.cellClicked.connect(self._cellCilicked)

        # 결제 버튼 및 최종 금액
        self.last_price = QLabel()
        self.last_price.setText("상품이 올려져 있지 않습니다.")
        self.last_price.setFont(QFont("맑은 고딕", 20))

        self.payment_button = QPushButton()
        self.payment_button.setText("결제하기")
        self.payment_button.setFixedWidth(100)

        self.payment_layout = QVBoxLayout()
        self.payment_layout.addWidget(self.last_price)
        self.payment_layout.addWidget(self.payment_button, alignment=Qt.AlignRight)

        return self.table, self.payment_layout

    def exShow(self, box):
        self.setLayout(box)
        self.setWindowTitle('Chart')
        self.move(300, 300)
        self.show()

    @pyqtSlot(list)
    def update_table_instances(self, ids):
        self.class_list = ids
        self.onlyone = set(self.class_list)
        self.table.setRowCount(len(self.onlyone))

        all_price = 0

        # 표 재설 정 반복문
        for row, class_id in enumerate(self.onlyone):
            # 각 요소들 초기화
            num = str(class_id)
            name = merchant_dictionary['name'][class_id]
            price = merchant_dictionary['price'][class_id]
            count = self.class_list.count(class_id)
            sum_price = count * int(price)
            all_price =  all_price + sum_price
            #print(num, name, price, count, sum_price)

            #print(num, name, price, count, sum_price)
            # 각 행에 추가
            self.table.setItem(row, 0, QTableWidgetItem(num))

            self.table.setItem(row, 1, QTableWidgetItem(name))

            # 숫자를 기준으로 정렬하기 위함. -- default 는 '문자'임.

            self.table.setItem(row, 2, QTableWidgetItem(format(int(price), ',') + '원'))

            self.m_count = QTableWidgetItem()
            self.m_count.setData(Qt.DisplayRole, str(count) + '개')
            self.table.setItem(row, 3, self.m_count)
            self.s_price = QTableWidgetItem()
            self.s_price.setData(Qt.DisplayRole, format(int(sum_price), ',') + '원')
            self.table.setItem(row, 4, self.s_price)

        self.last_price.setText("결제하실 금액은: " + format(int(all_price), ',') + '원'
                                + " 입니다.")



    def _cellCilicked(self, row, col):
        #print("cell_clicked = ", row, col)
        #print("clicked cell class id = ", self.table.item(row,0).text())
        if self.table.item(row, 0) != '':
            self.id_signal.emit(self.table.item(row, 0).text())
            self.name_signal.emit(self.table.item(row, 1).text())
            self.price_signal.emit(self.table.item(row, 2).text())

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = tableMaker()
    sys.exit(app.exec_())