import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class itemInfo(QWidget):

    def __init__(self):
        super().__init__()

        self.box = self.itemLayout()
        self.exShow(self.box)

    def itemLayout(self):
        self.image = QPixmap('../item_image/item1.png')

        self.lbl_img = QLabel()
        self.lbl_img.setPixmap(self.image)
        #self.lbl_size = QLabel('Width: '+str(self.image.width())+', Height: '+str(self.image.height()))
        self.lbl_size.setAlignment(Qt.AlignCenter)

        self.item_box = QVBoxLayout()
        self.item_box.addWidget(self.lbl_img)
        return self.item_box

    def exShow(self, box):
        self.setLayout(box)
        self.setWindowTitle('QPixmap')
        self.move(300, 300)
        self.show()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = itemInfo()
    sys.exit(app.exec_())