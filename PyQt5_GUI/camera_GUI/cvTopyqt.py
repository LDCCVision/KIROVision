# 웹캠의 영상을 받아서 pyqt에 보내준다.
# 소스 출처 https://github.com/baoboa/pyqt5/blob/master/examples/multimediawidgets/camera/camera.py

import cv2 # 오픈 cv 라이브러리
import sys
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui


class ShowVideo(QtCore.QObject):
    # 시그널을 정의하기 위해서는 QtCore.QObject를 상속해야한다.

    flag = 0

    camera = cv2.VideoCapture(0)
    # VideoCapture() 메소드를 사용해서 비디오 캡쳐 객체를 생성할 수 있다.
    # 메소드의 숫자는 어떤 카메라를 사용할 것 인가를 나타낸다.
    # 현재는 0이므로 0번 카메라를 사용한다(노트북 내장 캠)

    ret, image = camera.read()
    # cv.VideoCapture 메소드 객체의 read() 함수를 사용하면 영상을 읽을 수 있다.
    # 비디오를 한 프레임씩 읽는다.
    # 프레임을 읽을 수 있으면 True, 없으면 False를 반환한다.(반환은 ret)

    height, width = image.shape[:2]
    # image는 [3]인 크기를 가진다.
    # (높이, 너비, 채널)
    # 0~1까지의 데이터를 가지고 오므로 height, width를 차례로 가지고 온다.
    
    #print(image.shape)

    VideoSignal1 = QtCore.pyqtSignal(QtGui.QImage)
    VideoSignal2 = QtCore.pyqtSignal(QtGui.QImage)
    # pyqtSignal을 이용해서 사용자 정의 시그널을 생성
    # 신호의 type은 이미지이다.

    def __init__(self, parent=None):
        # 자식 클래스에서 부모클래스의 내용을 사용하고 싶을경우 오버라이드가 일어나지 않도록 해준다.
        super(ShowVideo, self).__init__(parent)

    @QtCore.pyqtSlot()
    # 슬롯을 만들기 위해서 사용하는 데코레이션
    def startVideo(self):
        global image
        # 함수 밖에 있는 변수 image를 불러옴

        run_video = True
        while run_video:
            ret, image = self.camera.read()
            color_swapped_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            # 무한반복되면서
            # 입력받은 영상을 프레임 단위의 이미지로 받는다
            # 받은 이미지를 처리하기 위해서 cvtColor 메소드 사용

            qt_image1 = QtGui.QImage(color_swapped_image.data,
                                    self.width,
                                    self.height,
                                    color_swapped_image.strides[0],
                                    QtGui.QImage.Format_RGB888)
            # color_swapped_image의 데이터를 pyqt에 보내기 위한 객체 설정
            self.VideoSignal1.emit(qt_image1)
            # 이 객체가 실행될때 신호 VideoSignal1으로 보낸다.


            if self.flag:
                # 만약 flag가 1이면 밑의 내용을 적용한다.
                img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                img_canny = cv2.Canny(img_gray, 50, 100)

                qt_image2 = QtGui.QImage(img_canny.data,
                                         self.width,
                                         self.height,
                                         img_canny.strides[0],
                                         QtGui.QImage.Format_Grayscale8)

                self.VideoSignal2.emit(qt_image2)


            loop = QtCore.QEventLoop()
            QtCore.QTimer.singleShot(25, loop.quit) #25 ms단위로 루프 결과를 가져옴
            loop.exec_()
            # 이벤트가 루프된다면 25ms단위로

    @QtCore.pyqtSlot()
    def canny(self):
        self.flag = 1 - self.flag


class ImageViewer(QtWidgets.QWidget):
    # 이미지를 보여주는 뷰어를 만든다.

    def __init__(self, parent=None):
        super(ImageViewer, self).__init__(parent)
        self.image = QtGui.QImage()
        self.setAttribute(QtCore.Qt.WA_OpaquePaintEvent)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawImage(0, 0, self.image)
        self.image = QtGui.QImage()

    def initUI(self):
        self.setWindowTitle('Test')

    @QtCore.pyqtSlot(QtGui.QImage)
    def setImage(self, image):
        # image는 VideoSignal1,2에서 보낸 신호에서 들어온것이다.
        if image.isNull():
            print("Viewer Dropped frame!")

        self.image = image
        # 받은 이미지를 이 클래스의 image 객체에 넣는다.
        if image.size() != self.size():
            self.setFixedSize(image.size())
            # 이미지와 이미지 뷰어의 크기가 다르다면 크기를 이미지 사이즈에 맞춘다.
        self.update()
        # 뷰어를 업데이트 해준다.


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)


    thread = QtCore.QThread()
    thread.start()
    # 스레드를 시작한다.
    vid = ShowVideo()
    vid.moveToThread(thread)
    # moveToThread 메소드
    # 부모를 가지고 있지 않은 객체에 대해서 사용가능
    # 객체 뿐 아니라 자식들까지 살아갈 스레드를 바꾼다.
    # vid 객체가 thread라는 스레드로 옮겨짐

    image_viewer1 = ImageViewer()
    image_viewer2 = ImageViewer()
    # 이미지 뷰어 객체 할당

    vid.VideoSignal1.connect(image_viewer1.setImage)
    vid.VideoSignal2.connect(image_viewer2.setImage)
    # VideoSignal1의 신호를 image_viewer1.setImage로 보낸다.

    push_button1 = QtWidgets.QPushButton('Start')
    push_button2 = QtWidgets.QPushButton('Canny')
    push_button1.clicked.connect(vid.startVideo)
    push_button2.clicked.connect(vid.canny)
    # 버튼 1,2를 만들어서 start, Canny라는 문자열을 붙혀준다.
    # 버튼 1을 클릭하면 클릭했다는 신호를 vid.startVideo로 보내준다.
    # 버튼 2번은 vid.canny로 신호를 보낸다.

    vertical_layout = QtWidgets.QVBoxLayout()
    horizontal_layout = QtWidgets.QHBoxLayout()
    horizontal_layout.addWidget(image_viewer1)
    horizontal_layout.addWidget(image_viewer2)
    vertical_layout.addLayout(horizontal_layout)
    vertical_layout.addWidget(push_button1)
    vertical_layout.addWidget(push_button2)
    # 레이아웃 설정

    layout_widget = QtWidgets.QWidget()
    layout_widget.setLayout(vertical_layout)
    # 위젯에 레이아웃을 넣음

    main_window = QtWidgets.QMainWindow()
    main_window.setCentralWidget(layout_widget)
    main_window.show()
    sys.exit(app.exec_())