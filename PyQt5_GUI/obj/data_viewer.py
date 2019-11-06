import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class dataViewer(QWidget):

    def __init__(self):
        super().__init__()

    def Layout(self):
        self.image = QPixmap()
        self.image.load('../user_image/NOT_LOGIN.png')

        self.lbl_img = QLabel()
        self.lbl_img.setPixmap(self.image)
        #self.lbl_size = QLabel('Width: '+str(self.image.width())+', Height: '+str(self.image.height()))
        #self.lbl_size.setAlignment(Qt.AlignCenter)

        #self.item_box = QVBoxLayout()
        #self.item_box.addWidget(self.lbl_img)
        return self.lbl_img

    def exShow(self, box):
        self.setLayout(box)
        self.setWindowTitle('QPixmap')
        self.move(300, 300)
        self.show()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = dataViewer()
    widet = ex.Layout()
    box = QVBoxLayout()
    box.addWidget(widet)
    ex.setLayout(box)
    ex.show()
    sys.exit(app.exec_())