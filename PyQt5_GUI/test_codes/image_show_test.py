from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys, cv2, numpy, time

class showImage(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        image = QLabel()
        image.resize(100, 100)
        image.setPixmap(QPixmap('../item1.jpg'))
        image.setScaledContents(True)
        image.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    test = showImage()
    test.show()
    sys.exit(app.exec_())