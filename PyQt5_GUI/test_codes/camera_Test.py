import sys
import cv2
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from modulelization.cameraAction import ShowVideo as ShowVideo
from modulelization.testWindow import *

column_idx_lookup = {'상품번호': 0, '상품명': 1, '가격': 2, '개수': 3, '총 금액': 4}

class ImageViewer(QWidget):
    def __init__(self, parent=None):
        super(ImageViewer, self).__init__(parent)
        self.image = QtGui.QImage()
        self.resize(self.image.size())
        self.setAttribute(QtCore.Qt.WA_OpaquePaintEvent)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawImage(0, 0, self.image)
        self.image = QtGui.QImage()

    def initUI(self):
        self.setWindowTitle('Test')

    @QtCore.pyqtSlot(QtGui.QImage)
    def setImage(self, image):
        global main_size
        if image.isNull():
            print("Viewer Dropped frame!")

        self.image = image.scaledToHeight(main_size.height() / 2.5)

        self.setFixedSize(self.image.size())

        self.update()

class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        # Window resize 이벤트 발생
        self.resized = Communicate()
        self.resized.signal.connect(self.update_to_window)

        # 카메라 이미지 뷰어 정의
        self.image_viewer0 = ImageViewer()
        self.image_viewer1 = ImageViewer()

        # itemImage, userImage 정의
        self.item_Label = QLabel()
        self.user_Label = QLabel()

        # Layout 정의
        self.item_data_layout = QVBoxLayout()
        self.user_data_layout = QVBoxLayout()

        self.initUI()

    def resizeEvent(self, event):
        self.resized.signal.emit()
        return super(MyApp, self).resizeEvent(event)

    def update_to_window(self):
        global main_size
        main_size = self.size()
        self.update_item_layout()
        self.update_user_layout()
        self.update_table_layout()

    def cellClicked(self, row, col):
        print("cellClicked... ", row, col)


    def set_item_table(self):

        itemtable = QTableWidget(4,5)

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
        #global itemtable
        self.itemtable.setColumnWidth(2, self.size().width() / 10)

    def load_user_layout(self):
        '''

        유저 데이터를 보여주는 레이아웃
        pixmap 객체로 사진을 가지고 오며, 아이디를 받아야되는것을 감안하여 아이디 변수를 설정하였다.

        '''

        pixmap = QtGui.QPixmap()
        pixmap.load('../user_image/user1.jpg')

        pixmap_resize = pixmap.scaled(self.size().width() / 16 * 9 / 2.5, self.size().width() / 16 * 9 / 2.5,
                                      QtCore.Qt.KeepAspectRatio)

        self.user_Label.setPixmap(pixmap_resize)

        user_name = QLabel()
        user_name.setText("황선태")

        user_payment = QLabel()
        user_payment.setText("card")

        self.user_data_layout.addWidget(self.user_Label, alignment=Qt.AlignCenter)
        self.user_data_layout.addWidget(user_name)
        self.user_data_layout.addWidget(user_payment)


    def update_user_layout(self):
        pixmap = QtGui.QPixmap()
        pixmap.load('../user_image/user1.jpg')

        pixmap_resize = pixmap.scaled(self.size().width() / 16 * 9 / 2.5, self.size().width() / 16 * 9 / 2.5,
                                      QtCore.Qt.KeepAspectRatio)

        self.user_Label.setPixmap(pixmap_resize)

    def load_item_layout(self):
        pixmap = QtGui.QPixmap('../item_image/item1.png')
        pixmap_resize = pixmap.scaled(self.size().width() / 16 * 9 / 2.5, self.size().width() / 16 * 9 / 2.5,
                                      QtCore.Qt.KeepAspectRatio)

        self.item_Label.setPixmap(pixmap_resize)

        self.item_data_layout.addWidget(self.item_Label, alignment=Qt.AlignCenter)

        item_name = QLabel()
        item_name.setText("꼬깔콘")

        item_payment = QLabel()
        item_payment.setText("1500")

        self.item_data_layout.addWidget(item_name)
        self.item_data_layout.addWidget(item_payment)

    def update_item_layout(self):
        pixmap = QtGui.QPixmap('../item_image/item1.png')
        pixmap_resize = pixmap.scaled(self.size().width() / 16 * 9 / 2.5, self.size().width() / 16 * 9 / 2.5,
                                      QtCore.Qt.KeepAspectRatio)

        self.item_Label.setPixmap(pixmap_resize)

    def initUI(self):
        global main_size

        self.setGeometry(100, 100, 1600, 900)
        main_size = QSize(1600, 900)

        self.itemtable = self.set_item_table()

        connect_box = QHBoxLayout()
        camera_box = QVBoxLayout()
        data_box = QVBoxLayout()

        camera_box.addWidget(self.image_viewer0)
        camera_box.addWidget(self.image_viewer1)

        self.load_item_layout()
        self.load_user_layout()

        data_box.addLayout(self.item_data_layout)  # 상품에 대한 정보는 아직 레이아웃이 만들어지짖 않았기 때문에 라벨 데이터로 대신한다.
        data_box.addLayout(self.user_data_layout)

        connect_box.addLayout(camera_box)
        connect_box.addLayout(data_box)
        connect_box.addWidget(self.itemtable)

        self.setLayout(connect_box)

        self.setWindowTitle('GUI')

        self.show()

# 조건 없이 이벤트를 emit하는 클래스
class Communicate(QObject):
    signal = pyqtSignal()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_size = QSize()

    test = Test()
    ex = MyApp()
    # 카메라 사용 중지를 위한 주석처리 2/2

    thread = QtCore.QThread()
    thread.start()
    # 스레드를 시작한다.
    vid = ShowVideo()
    vid.moveToThread(thread)
    # moveToThread 메소드
    # 부모를 가지고 있지 않은 객체에 대해서 사용가능
    # 객체 뿐 아니라 자식들까지 살아갈 스레드를 바꾼다.
    # vid 객체가 thread라는 스레드로 옮겨짐

    # 이미지 뷰어 객체 할당

    vid.FVideoSignal.connect(ex.image_viewer0.setImage)
    vid.CVideoSignal.connect(ex.image_viewer1.setImage)

    showViewfinder = Communicate()
    showViewfinder.signal.connect(vid.startVideo)
    showViewfinder.signal.emit()

    sys.exit(app.exec_())
