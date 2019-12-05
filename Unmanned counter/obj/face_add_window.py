from PyQt5.QtWidgets import QWidget, QApplication, QLineEdit, QPushButton, QVBoxLayout, QDialog, QHBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal

import obj.signUp as signUp

import sys

class face_add(QDialog):

    name_signal = pyqtSignal(str)
    id_signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super(face_add, self).__init__(parent)

        self.window_set()


    def window_set(self):
        # 윈도우의 크기를 설정
        print("실행됬습니다.")
        self.resize(160, 90)

        # 이름 등록부분
        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("아이디를 입력해주세요")
        
        # 버튼 레이아웃 설정
        self.start_btn = QPushButton()
        self.start_btn.setText("등록 시작")

        self.btn_layout = QHBoxLayout()
        #self.btn_layout.addWidget(self.sign_up_btn)
        self.btn_layout.addWidget(self.start_btn)
        
        # 팝업창 설정
        self.window = QVBoxLayout()
        self.window.addWidget(self.id_input)
        #self.window.addWidget(self.password_input)
        self.window.addLayout(self.btn_layout)
        self.setLayout(self.window)

        self.show()
        
        # 버튼 클릭 신호 연결부
        self.start_btn.clicked.connect(self.buttonEvent)

    def buttonEvent(self):
        # 버튼 클릭시 이름 전송
        id = self.id_input.text()
        self.name_signal.emit(id)
        self.done(QDialog.Accepted)
    '''
    def signUp(self):
        id = self.id_input.text()
        self.signup = signUp.signUp()
        self.signup.idInput(id)
        self.signup.checkIdOverlap()
        self.done(QDialog.Accepted)
        self.signup.exec_()
    '''

'''
if __name__ == "__main__":
    app = QApplication([])
    ex = face_add()
    ex.show()
    sys.exit(app.exec_())
'''