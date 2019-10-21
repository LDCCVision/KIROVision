from PyQt5 import QtCore
from PyQt5 import QtGui

import cv2

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