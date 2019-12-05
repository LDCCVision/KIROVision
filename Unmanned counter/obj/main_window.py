import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from PyQt5.QtWidgets import QBoxLayout, QGroupBox, QMainWindow, QApplication, QWidget,QTableWidget, QDesktopWidget, QGridLayout, QLabel, QLineEdit, QTextEdit, QVBoxLayout,QHBoxLayout, QPushButton
from PyQt5.QtCore import QThread, QObject, pyqtSignal, QSize, pyqtSlot, Qt, QThreadPool
from PyQt5.QtGui import QPixmap, QFont

import obj.data_viewer as dataView
import obj.chart as tableSetting
import obj.imageViewer as imageViewer
import obj.showVideo as showVideo
import obj.face_add_window as faceAddWindow

class Communicate_int(QObject):
    signal = pyqtSignal(int)

class Communicate(QObject):
    signal = pyqtSignal()

class mainWindow(QWidget):

    cell_clicked = False
    login_start = False
    item_image_name = "NOT_LOGIN"
    user_image_name = "NOT_LOGIN"
    login = False

    user_image_list = os.listdir("../user_image/")
    id = None
    id_image = str
    act = -1

    def __init__(self):
        super().__init__()

        self.resized = Communicate()
        self.resized.signal.connect(self.update_window)
        
        # 크기를 보내주는 신호 설정
        self.FsendWidth = Communicate_int()
        self.MsendWidth = Communicate_int()

        # 레이아웃 결합
        self.main_layout = self.setLayout(self.createAllLayout())
        self.show()

        self.startVideo()

    def resizeEvent(self, event):
        self.resized.signal.emit()
        return super(mainWindow, self).resizeEvent(event)

    @pyqtSlot()
    def update_window(self):

        sending_height = self.size().height()

        self.updateDataLayout()
        self.update_table_layout()

        self.FsendWidth.signal.emit(sending_height)
        self.MsendWidth.signal.emit(sending_height)

    def updateDataLayout(self):

        user_path = '../user_image/'

        if self.login_start == True:
            user_name = self.user_image_name + '.png'
        else:
            user_name = "Not_LOGIN" + '.png'

        pixmap = QPixmap()
        pixmap.load(user_path + user_name)
        pixmap_resize = pixmap.scaled(self.size().width() / 16 * 9 / 3, self.size().width() / 16 * 9 / 3,
                                      Qt.KeepAspectRatio)

        self.user_widget.setPixmap(pixmap_resize)

        item_path = '../item_image/'
        if self.cell_clicked == True:
            item_name = self.item_image_name + '.jpg'
        else:
            item_name = "Not_LOGIN" + '.png'

        pixmap = QPixmap()
        pixmap.load(item_path + item_name)
        pixmap_resize = pixmap.scaled(self.size().width() / 16 * 9 / 3, self.size().width() / 16 * 9 / 3,
                                      Qt.KeepAspectRatio)

        self.item_widget.setPixmap(pixmap_resize)

    def update_table_layout(self):
        self.table.setColumnWidth(2, self.size().width() / 10)

    def addBtnClicked(self):
        add_window = faceAddWindow.face_add()
        add_window.name_signal.connect(self.video.inputName)
        add_window.exec_()

    def returnIdAct(self, id):
        self.id = id
        if id == "Unknown": # 얼굴이 등록이 안되있을경우
            self.act = 0
        elif self.id + '.png' in self.user_image_list: # 등록이 되어있고 사진이 있을 경우
            self.act = 1
        else: # 등록이 되어있지만 사진이 없을 경우
            self.act = 2

    def loginBtnCliked(self):
        self.login = True
        if self.act == 0: # 얼굴이 등록이 안되있을경우
            self.user_name_label.setText("등록이 되지 않은 사용자입니다.\n 얼굴 등록을 해주십시요")
        elif self.act == 1: # 등록이 되어있고 사진이 있을 경우
            self.login_start = True
            self.user_name_label.setText(self.id + "님으로 로그인 되었습니다.")
            self.user_image_name = self.id
            self.updateDataLayout()
        else: # 등록이 되어있지만 사진이 없을 경우
            self.login_start = True
            self.user_name_label.setText(self.id + "님으로 로그인 되었습니다.")
            self.user_image_name = "NOT_LOGIN"
        print(self.act)

    def takePicture(self):

        if self.login == False:
            self.user_name_label.setText("로그인이 필요합니다.")
        elif self.id == "Unknown":
            self.user_name_label.setText("얼굴 등록 후 로그인을 해주세요.")
        else:
            self.video.picture_signal.emit()
            self.updateDataLayout()

    def createAllLayout(self):
        # 창은 16:9 비율로 제작
        self.setWindowTitle('MainWindow')

        self.resize(940, 450)
        #self.resize(1600,900)
        self.set_center()

        # 비디오 뷰어 설정
        self.face_viewer = imageViewer.imageViewer()
        self.FsendWidth.signal.connect(self.face_viewer.setAncorSize)
        self.FsendWidth.signal.emit(self.size().width())
        self.face_add_bnt = QPushButton("얼굴 등록하기")

        self.face_add_bnt.clicked.connect(self.addBtnClicked)

        self.merchant_viewer = imageViewer.imageViewer()
        self.MsendWidth.signal.connect(self.merchant_viewer.setAncorSize)
        self.MsendWidth.signal.emit(self.size().width())

        self.button_layout = QVBoxLayout()
        self.button_layout.addWidget(self.face_add_bnt, alignment=Qt.AlignRight)

        self.Fvideo_layout = QVBoxLayout()
        self.Fvideo_layout.addWidget(self.face_viewer)
        self.Fvideo_layout.addLayout(self.button_layout)

        self.Fvideo_group = QGroupBox()
        self.Fvideo_group.setTitle("얼굴인식 카메라")
        self.Fvideo_group.setLayout(self.Fvideo_layout)

        self.Mvideo_layout = QVBoxLayout()
        self.Mvideo_layout.addWidget(self.merchant_viewer)

        self.Mvideo_group = QGroupBox()
        self.Mvideo_group.setTitle("상품인식 카메라")
        self.Mvideo_group.setLayout(self.Mvideo_layout)

        self.video_layout = QVBoxLayout()
        self.video_layout.addWidget(self.Fvideo_group)
        self.video_layout.addWidget(self.Mvideo_group)

        # 아이템 뷰어 설정
        self.item_viewer = dataView.dataViewer()
        self.item_widget = self.item_viewer.Widget()
        self.item_name_label = self.item_viewer.nameLabel()
        self.item_name_label.setText("상품 이름:")
        self.item_price_label = self.item_viewer.priceLabel()

        self.item_layout = QVBoxLayout()
        self.item_layout.addWidget(self.item_widget)
        self.item_layout.addWidget(self.item_name_label)
        self.item_layout.addWidget(self.item_price_label)


        self.item_group = QGroupBox()
        self.item_group.setTitle("상품 정보")
        self.item_group.setLayout(self.item_layout)

        # 유저 뷰어 설정
        self.user_viewer = dataView.dataViewer()
        self.user_widget = self.user_viewer.Widget()
        
        self.user_name_label = self.item_viewer.nameLabel()
        self.user_name_label.setText("로그인이 필요합니다.")
        
        self.user_recog_btn = QPushButton()
        self.user_recog_btn.setText("로그인하기")
        self.user_recog_btn.clicked.connect(self.loginBtnCliked)

        self.take_picture_btn = QPushButton()
        self.take_picture_btn.setText("사진 변경")
        self.take_picture_btn.clicked.connect(self.takePicture)


        self.user_layout = QVBoxLayout()
        self.user_layout.addWidget(self.user_widget, alignment= Qt.AlignCenter)
        self.user_layout.addWidget(self.user_name_label)
        self.user_layout.addWidget(self.take_picture_btn)
        self.user_layout.addWidget(self.user_recog_btn, alignment=Qt.AlignRight)

        self.user_group = QGroupBox()
        self.user_group.setTitle("회원 정보")
        self.user_group.setLayout(self.user_layout)

        # 아이템 테이블 설정
        self.table_maker = tableSetting.tableMaker()
        self.table_maker.show_change.connect(self.updateDataLayout)
        self.table_maker.name_signal.connect(self.changeItemName)
        self.table_maker.price_signal.connect(self.changeItemPrice)
        self.table_maker.id_signal.connect(self.changeItemImage)
        self.table, self.payment_layout = self.table_maker.setTable()


        self.tabel_layout = QVBoxLayout()
        self.tabel_layout.addWidget(self.table)

        # 레이아웃을 세로 방향 레이아웃 3개로 제작

        # 좌측 레이아웃 설정
        #self.left_layout = QVBoxLayout()
        #self.left_layout.addLayout(self.video_layout)

        self.video_group = QGroupBox()
        self.video_group.setTitle("video_group")
        self.video_group.setLayout(self.video_layout)
        
        # 중앙 레이아웃 설정
        self.center_layout = QVBoxLayout()
        self.center_layout.addWidget(self.user_group)
        self.center_layout.addWidget(self.item_group)

        self.data_group = QGroupBox()
        self.data_group.setTitle("data_group")
        self.data_group.setLayout(self.center_layout)

        # 우측 레이아웃 설정
        self.right_layout = QVBoxLayout()
        self.right_layout.addLayout(self.tabel_layout)
        self.right_layout.addLayout(self.payment_layout)

        self.table_group = QGroupBox()
        self.table_group.setTitle("table_group")
        self.table_group.setLayout(self.right_layout)

        # 전체 레이아웃 결합
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.video_group)
        self.layout.addWidget(self.data_group)
        self.layout.addWidget(self.table_group)

        return self.layout

    def changeItemImage(self, class_id):
        self.cell_clicked = True
        self.item_image_name = str(class_id)

        item_path = '../item_image/'
        if self.cell_clicked == True:
            item_name = self.item_image_name + '.jpg'
        else:
            item_name = "NOT_LOGIN" + '.png'

        pixmap = QPixmap()
        pixmap.load(item_path + item_name)
        pixmap_resize = pixmap.scaled(self.size().width() / 16 * 9 / 2.5, self.size().width() / 16 * 9 / 2.5,
                                      Qt.KeepAspectRatio)

        self.item_widget.setPixmap(pixmap_resize)

    def changeItemName(self, m_name):
        self.item_name = str(m_name)

        pre_text = "상품 이름: "
        self.item_name_label.setText(pre_text + self.item_name)

    def changeItemPrice(self, m_price):
        self.item_price = str(m_price)

        pre_text = "상품 가격: "
        self.item_price_label.setText(pre_text + self.item_price)


    def set_center(self):
        # 모니터 중앙에 창을 표시해줌
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def startVideo(self):
        self.video_thread = QThread()
        self.video_thread.start()

        self.video = showVideo.VideoViewer()
        self.video.moveToThread(self.video_thread)

        self.video.id_signal.connect(self.table_maker.update_table_instances)
        self.video.videoSignal.connect(self.face_viewer.setImage)
        self.video.Mvideo_signal.connect(self.merchant_viewer.setImage)
        self.video.user_id_signal.connect(self.returnIdAct)
        self.video.picture_signal.connect(self.video.takePicuture)
        print("이미지 전송 시그널 설정 완료")

        self.video.startVideo()
        print("얼굴 이미지 송출 시작")



if __name__ == "__main__":
    app = QApplication([])
    ex = mainWindow()
    sys.exit(app.exec_())