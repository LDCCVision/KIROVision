# Unmanned counter Project

# 무인 계산대 프로젝트

## 1. Abstract

[시연영상[YouTube]](https://youtu.be/XbMtUq8GAPM) "자막에 영상에 대한 설명을 넣었습니다."

---

> #### 사물인식과 얼굴인식 딥러닝 모델을 이용한 무인 계산대 프로젝트입니다.
> **Object detection** 모델을 이용하여 계산대에 올려진 상품들을 자동으로 인식한 후, 
> **Face recognition** 모델을 이용하여 구매자를 인식하여 
> 무인 계산대에서 쉽고 빠르게 결제를 처리할 수 있습니다. 

YOLO_v3와 FaceNet이 사용되었습니다.

인식할 수 있는 상품의 종류는 51가지이며 
상품의 목록은 `Unmanned counter/data/classes/label.txt` 파일을 참고하세요.

얼굴인식 모델엔 구매자 얼굴 등록 및 로그인 기능이 구현되어 있습니다.
등록된 구매자의 얼굴 사진은 `Unmanned counter/user_image`에 저장됩니다.

## 2. requirement

### 1) 환경 셋팅

PyCharm IDE에서 실행할 것을 권장합니다.
아래 표은 개발 당시의 주요 파이썬 패키지의 버전 목록입니다.
표기된 버전의 상위 버전 패키지를 사용하시고 
에러가 발생한다면 아래의 버전으로 다운그레이드하세요.

tensorflow 2.x 버전대는 호환되지 않습니다.

| Package        | Version |
| -------------- | ------- |
| numpy          | 1.15.1  |
| pillow         | 5.3.0   |
| scipy          | 1.1.0   |
| tensorflow-gpu | 1.13.1  |
| wget           | 3.2     |
| seaborn        | 0.9.0   |
| pyqt           | 5.9.2   |
| easydict       | 1.9     |

### 2) 파일 복사

오른쪽 링크에서 압축파일을 다운로드합니다. [[Link]](https://drive.google.com/file/d/1cNmUbdONFoG3fmHxGyhcN5Fw7sR92c4g/view?usp=sharing)

`Facenet` 폴더, `checkpoint ` 폴더, `yolov3_coco.pb`를 `Unmanned counter` 폴더에 복사해주세요.

## 3. How to run this model

`Unmanned counter/obj/main_window.py` 파일을 실행하세요.

초기 설정으로 테스트 영상으로 모델이 작동합니다.
웹캠을 사용하시려면 `Unmanned counter/obj/showVideo.py`의 41번 라인을 참고하세요.

기타 궁금한 점이나 문의사항이 있으시다면 koo9water@gmail.com로 연락주세요.

