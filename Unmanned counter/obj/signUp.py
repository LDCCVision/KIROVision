import numpy as np

from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal

class signUp(QDialog):
    id_path = '../data/userId/user_dic.npy'
    ids = np.load(id_path)
    id = str

    recall_signal = pyqtSignal()

    def __init__(self, parent=None):
        super(signUp, self).__init__(parent)

    def setWindow(self):
        # 윈도우의 크기를 설정
        self.checkIdOverlap()

    def showOverlapError(self):
        # 아이디가 중복이면 중복 팝업창을 띄운다.
        self.resize(480, 270)
        self.error_message = QLabel()
        self.error_message.setText("이미 사용중인 아이디 입니다.\n다른 아이디를 사용해 주세요")

        self.Cbtn = self.setConfrimBtn()

        self.error_layout = QVBoxLayout()
        self.error_layout.addWidget(self.error_message, alignment=Qt.AlignCenter)
        self.error_layout.addWidget(self.Cbtn)

        self.setLayout(self.error_layout)
        self.show()

    def setConfrimBtn(self):
        self.confirm_btn = QPushButton()
        self.confirm_btn.setText("확인")
        self.confirm_btn.clicked.connect(self.confirmBtnClicked)
        return self.confirm_btn

    def confirmBtnClicked(self):
        self.done(QDialog.Accepted)

    def confirmSignUp(self):
        self.resize(160, 90)
        self.success_message = QLabel()
        self.success_message.setText("회원가입 되었습니다!")

        self.Cbtn = self.setConfrimBtn()

        self.success_layout = QVBoxLayout()
        self.success_layout.addWidget(self.success_message, alignment=Qt.AlignCenter)
        self.success_layout.addWidget(self.Cbtn)

        self.setLayout(self.success_layout)
        self.show()

    def idAdd(self):
        self.ids = np.append(self.ids, self.id)
        np.save(self.id_path, self.ids)

    def checkIdOverlap(self):
        print(self.id)
        if self.id in self.ids:
            # id가 이미 class_names에 있으면
            self.showOverlapError()
        else:
            self.idAdd()
            self.confirmSignUp()
        print(self.ids)

    def idInput(self, id):
        self.id = id
        print(self.id)