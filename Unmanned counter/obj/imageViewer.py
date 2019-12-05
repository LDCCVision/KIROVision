import sys
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QImage
from PyQt5 import QtCore
from PyQt5.QtCore import Qt

class imageViewer(QWidget):
    def __init__(self, parent=None):
        super(imageViewer, self).__init__(parent)
        self.image = QImage()

    @QtCore.pyqtSlot(int)
    def setAncorSize(self, anchor):
        self.anchor = anchor

    def paintEvent(self, event):
        # 0,0을 기준으로 이미지를 그려주는 이벤트 창
        # 이벤트로 그림을 그려주고 이미지창을 초기화해준다.
        painter = QPainter(self)
        painter.drawImage(0, 0, self.image)
        self.image = QImage()

    def initUI(self):
        self.setWindowTitle('VideoVidwer')

    @QtCore.pyqtSlot(QImage)
    def setImage(self, image):
        # 이미지를 시그널로 받아와서 창에 띄워준다.
        if image.isNull():
            # 이미지를 받지 못했다면
            print("Viewer Dropped Frame!")
        try:
            self.image = image.scaledToHeight(self.anchor / 2.5)
            #print(image.size())
            self.setFixedSize(self.image.size())
            self.update()
        except Exception as e:
            print("에러 발생")
            pass
