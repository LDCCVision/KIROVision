import sys
from PyQt5.QtWidgets import QApplication, QWidget,QTableWidget, QDesktopWidget, QGridLayout, QLabel, QLineEdit, QTextEdit, QVBoxLayout,QHBoxLayout
from PyQt5.QtCore import QThread, QObject, pyqtSignal, QSize, pyqtSlot, Qt, QThreadPool
from PyQt5.QtGui import QPixmap

import obj.data_viewer as dataView
import obj.chart as tableSetting
import obj.imageViewer as imageViewer
import obj.showVideo as showVideo

class Communicate_int(QObject):
    signal = pyqtSignal(int)

class Communicate(QObject):
    signal = pyqtSignal()

class mainWindow(QWidget):

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
        print("창 크기가 변경됨")

        sending_height = self.size().height()

        self.updateDataLayout()
        self.update_table_layout()

        self.FsendWidth.signal.emit(sending_height)
        self.MsendWidth.signal.emit(sending_height)

        print(self.size().width(), self.size().height())

    def updateDataLayout(self):

        pixmap = QPixmap()
        pixmap.load('../user_image/NOT_LOGIN.png')
        pixmap_resize = pixmap.scaled(self.size().width() / 16 * 9 / 2.5, self.size().width() / 16 * 9 / 2.5,
                                      Qt.KeepAspectRatio)

        self.item_widget.setPixmap(pixmap_resize)

        pixmap = QPixmap()
        pixmap.load('../user_image/NOT_LOGIN.png')
        pixmap_resize = pixmap.scaled(self.size().width() / 16 * 9 / 2.5, self.size().width() / 16 * 9 / 2.5,
                                      Qt.KeepAspectRatio)

        self.user_widget.setPixmap(pixmap_resize)

    def update_table_layout(self):
        self.table.setColumnWidth(2, self.size().width() / 10)

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

        self.merchant_viewer = imageViewer.imageViewer()
        self.MsendWidth.signal.connect(self.merchant_viewer.setAncorSize)
        self.MsendWidth.signal.emit(self.size().width())

        self.video_layout = QVBoxLayout()
        self.video_layout.addWidget(self.face_viewer)
        self.video_layout.addWidget(self.merchant_viewer)

        # 버튼 뷰어 설정


        # 아이템 뷰어 설정
        self.item_viewer = dataView.dataViewer()
        self.item_widget = self.item_viewer.Layout()

        # 유저 뷰어 설정
        self.user_viewer = dataView.dataViewer()
        self.user_widget = self.user_viewer.Layout()

        # 아이템 테이블 설정
        self.table_maker = tableSetting.tableMaker()
        self.table = self.table_maker.setTable()

        # 레이아웃을 세로 방향 레이아웃 3개로 제작

        # 좌측 레이아웃 설정
        self.left_layout = QVBoxLayout()
        self.left_layout.addLayout(self.video_layout)
        
        # 중앙 레이아웃 설정
        self.center_layout = QVBoxLayout()
        self.center_layout.addWidget(self.item_widget)
        self.center_layout.addWidget(self.user_widget)

        # 우측 레이아웃 설정
        self.right_layout = QVBoxLayout()
        self.right_layout.addWidget(self.table)

        # 전체레이아웃 결합
        self.layout = QHBoxLayout()
        self.layout.addLayout(self.left_layout)
        self.layout.addLayout(self.center_layout)
        self.layout.addLayout(self.right_layout)

        return self.layout

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
        print("이미지 전송 시그널 설정 완료")

        self.video.startVideo()
        print("얼굴 이미지 송출 시작")
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = mainWindow()
    sys.exit(app.exec_())