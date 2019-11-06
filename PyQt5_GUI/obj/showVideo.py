import cv2
from PIL import Image

from PyQt5 import QtCore, QtGui

# 스레드를 사용해서 영상 정보를 QObject로 받는 VideoViewer 설정

class VideoViewer(QtCore.QObject):
    '''카메라 뷰어'''
    # opencv 사용
    # 클래스안의 전역변수로 사용되는 변수들 설정
    
    # 비디오 캡쳐를 이용해서 0번 카메라의 객체를 생성
    camera = cv2.VideoCapture(0)
    m_camera = cv2.VideoCapture(0)

    # 이미지를 잘 받았는지, 어떤 이미지인지를 반환하는 함수 read()를 사용하여 프레임을 카메라로부터 받아온다.
    ret, image = camera.read()
    
    # 이미지의 높이, 너비를 shape로부터 받아옴
    height, width = image.shape[:2]

    # 이미지를 시그널로 보냄
    videoSignal = QtCore.pyqtSignal(QtGui.QImage)
    Mvideo_signal = QtCore.pyqtSignal(QtGui.QImage)
    id_signal = QtCore.pyqtSignal(list)

    #---------------------------------------------- 전역 변수 설정 완료 --------------------
    
    def __init(self, parent=None):
        super(VideoViewer, self).__init__(parent)

    #@QtCore.pyqtSlot()
    def startVideo(self):
        global image

        run_video = True

        while run_video:
            # 비디오가 참일때만
            # 얼굴 이미지
            ret, image = self.camera.read()
            #print(image)
            image = cv2.flip(image, 1)
            color_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            qt_image = QtGui.QImage(color_image,
                                    self.width,
                                    self.height,
                                    color_image.strides[0],
                                    QtGui.QImage.Format_RGB888
            )

            # 이미지를 비디오 시그널로 보낸다.
            #print(qt_image.size())
            self.videoSignal.emit(qt_image)

            # 상품 이미지
            #m_ret, m_image = self.m_camera.read()
            m_image = image
            m_color_image = cv2.cvtColor(m_image, cv2.COLOR_BGR2RGB)

            m_qt_image = QtGui.QImage(m_color_image,
                                    self.width,
                                    self.height,
                                    m_color_image.strides[0],
                                    QtGui.QImage.Format_RGB888
                                    )

            # 이미지를 비디오 시그널로 보낸다.
            #print(qt_image.size())

            test = [1,2,3,4,5]
            self.Mvideo_signal.emit(m_qt_image)
            self.id_signal.emit(test)

            # 이벤트를 루프 시킨다.
            # 25ms 단위로 루프 결과를 가져온다.
            loop = QtCore.QEventLoop()
            QtCore.QTimer.singleShot(25, loop.quit)
            loop.exec()

