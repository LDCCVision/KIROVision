import sys
import cv2
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import *

column_idx_lookup = {'상품번호': 0, '상품명': 1, '가격': 2, '개수': 3, '총 금액': 4}

user_dic = {'user_number' : [-1, 0, 1, 2, 3],
            'user_image_name' : ['NOT_LOGIN.png', 'user1.jpg','user2.jpg', 'user3.jpg', 'user4.jpg'],
            'user_name' : ['unknown', '황선태','박경훈','구정수','홍길동']}

user_number = user_dic['user_number'][0]
user_image_name = user_dic['user_image_name'][0]
user_name = user_dic['user_name'][0]

class ShowVideo(QtCore.QObject):
    '''
        얼굴인식 카메라를 0번
        카운터 카메라를 2번으로 설정
        카운터 카메라를 연결했을경우 주석을 지우고 카메라 아이디를 맞춰줄것
    '''

    # 카메라 사용 중지를 위한 주석처리 1/2

    face_camera = cv2.VideoCapture(0)
    counter_camera = cv2.VideoCapture(0)

    face_ret, face_image = face_camera.read()
    counter_ret, counter_image = counter_camera.read()

    Fheight, Fwidth = face_image.shape[:2]
    Cheight, Cwidth = counter_image.shape[:2]

    FVideoSignal = QtCore.pyqtSignal(QtGui.QImage)
    CVideoSignal = QtCore.pyqtSignal(QtGui.QImage)

    def __init__(self, parent=None):
        super(ShowVideo, self).__init__(parent)

    @QtCore.pyqtSlot()
    def startVideo(self):
        global face_image, counter_image

        run_video = True

        while run_video:
            face_ret, face_image = self.face_camera.read()
            counter_ret, counter_image = self.counter_camera.read()

            Fcolor_swapped_image = cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB)
            Ccolor_swapped_image = cv2.cvtColor(counter_image, cv2.COLOR_BGR2RGB)
            # 무한반복되면서
            # 입력받은 영상을 프레임 단위의 이미지로 받는다
            # 받은 이미지를 처리하기 위해서 cvtColor 메소드 사용

            qt_image1 = QtGui.QImage(Fcolor_swapped_image.data,
                                     self.Fwidth,
                                     self.Fheight,
                                     Fcolor_swapped_image.strides[0],
                                     QtGui.QImage.Format_RGB888)
            # color_swapped_image의 데이터를 pyqt에 보내기 위한 객체 설정
            self.FVideoSignal.emit(qt_image1)
            # 이 객체가 실행될때 신호 VideoSignal1으로 보낸다.

            qt_image2 = QtGui.QImage(Ccolor_swapped_image.data,
                                     self.Cwidth,
                                     self.Cheight,
                                     Ccolor_swapped_image.strides[0],
                                     QtGui.QImage.Format_RGB888)
            # color_swapped_image의 데이터를 pyqt에 보내기 위한 객체 설정
            self.CVideoSignal.emit(qt_image2)
            # 이 객체가 실행될때 신호 VideoSignal2으로 보낸다.

            loop = QtCore.QEventLoop()
            QtCore.QTimer.singleShot(25, loop.quit)  # 25 ms단위로 루프 결과를 가져옴
            loop.exec_()


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

        # self.setSizePolicy(1, 1)
        # self.resize(main_size/3)
        # self.image.scaled(main_size.width() / 3, main_size.width(), QtCore.Qt.KeepAspectRatio)

        self.setFixedSize(self.image.size())

        # self.setFixedSize(selfWidth, selfHeight)
        # if image.size() != self.size():
        #    self.setFixedSize(image.size())

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

    @QtCore.pyqtSlot()
    def update_to_window(self):
        global main_size
        main_size = self.size()
        self.update_item_layout()
        self.update_user_layout()
        self.update_table_layout()

    def cellClicked(self, row, col):
        print("cellClicked... ", row, col)

    def set_item_table(self):
        global itemtable

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
        global itemtable
        itemtable.setColumnWidth(2, self.size().width() / 10)

    def load_user_layout(self):
        '''

        유저 데이터를 보여주는 레이아웃
        pixmap 객체로 사진을 가지고 오며, 아이디를 받아야되는것을 감안하여 아이디 변수를 설정하였다.

        '''

        self.user_pixmap = QtGui.QPixmap()
        self.user_pixmap.load('../user_image/' + user_image_name)

        pixmap_resize = self.user_pixmap.scaled(self.size().width() / 16 * 9 / 2.5, self.size().width() / 16 * 9 / 2.5,
                                      QtCore.Qt.KeepAspectRatio)
        
        self.user_Label.setPixmap(pixmap_resize)

        self.user_name_label = QLabel()
        self.user_name_label.setText(user_name)

        user_payment_label = QLabel()
        user_payment_label.setText("card")

        self.user_data_layout.addWidget(self.user_Label, alignment=Qt.AlignCenter)
        self.user_data_layout.addWidget(self.user_name_label)
        self.user_data_layout.addWidget(user_payment_label)

    def update_user_layout(self):

        global user_image_name, user_name
        print(user_number, user_name, user_image_name)

        pixmap = QtGui.QPixmap()
        pixmap.load('../user_image/' + user_image_name)

        pixmap_resize = pixmap.scaled(self.size().width() / 16 * 9 / 2.5, self.size().width() / 16 * 9 / 2.5,
                                      QtCore.Qt.KeepAspectRatio)

        self.user_Label.setPixmap(pixmap_resize)
        self.user_name_label.setText(user_name)

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
        connect_box.addWidget(self.set_item_table())

        self.setLayout(connect_box)

        self.setWindowTitle('GUI')

        self.show()


# 추후 테스트를 위해 테이블에 데이터를 입력하기 위한 별도의 Widget

class Test(QWidget):
    def __init__(self):
        super().__init__()
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
        global itemtable
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
        global itemtable
        row_count = itemtable.rowCount()

        while True:
            state = 0
            for i in range(row_count - 1):
                if self.deleteIdx.text() == temp.text():
                    itemtable.removeRow(i)
                    state = 1
                    i = i - 1

            if state == 0: return


class SendUserData(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.input_button = QPushButton("&INPUT")
        self.input_line = QLineEdit()
        self.input_line.setPlaceholderText("테스트 할 손님의 번호를 입력")

        main_box = QVBoxLayout()
        main_box.addWidget(self.input_line)
        main_box.addWidget(self.input_button)

        self.setLayout(main_box)

        self.setWindowTitle('Sending_user_data')
        self.setGeometry(300, 300, 300, 200)
        self.show()


        # submit 버튼을 누르면 이벤트 발생
        self.input_button.clicked.connect(self.inputButtonPush)

    @QtCore.pyqtSlot()
    def inputButtonPush(self):
        global user_number, user_name, user_image_name
        self.user_number = int(self.input_line.text()) +1
        user_number = user_dic['user_number'][self.user_number]
        user_name = user_dic['user_name'][self.user_number]
        user_image_name = user_dic['user_image_name'][self.user_number]

        print(self.user_number)
        print(user_number, user_name, user_image_name)

        global update
        update.signal.emit()






# 조건 없이 이벤트를 emit하는 클래스
class Communicate(QObject):
    signal = pyqtSignal()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    itemtable = QTableWidget(4, 5)
    main_size = QSize()

    test = Test()
    user_data_send = SendUserData()
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

    update = Communicate()
    update.signal.connect(ex.update_to_window)

    sys.exit(app.exec_())


# test2