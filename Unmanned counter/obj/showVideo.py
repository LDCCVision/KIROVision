import cv2
from PIL import ImageDraw,ImageFont,Image
import os
import numpy as np
import pickle
from sklearn.svm import SVC
import sys
import time
import math
import tensorflow as tf
import core.utils as utils
from PyQt5 import QtCore, QtGui

import Facenet.contributed.face as face

# Object Detection Model에 필요한 hyper parameter
return_elements = ["input/input_data:0", "pred_sbbox/concat_2:0", "pred_mbbox/concat_2:0", "pred_lbbox/concat_2:0"]
pb_file         = "../yolov3_coco.pb"
#video_path      = "./docs/images/road.mp4"
video_path      = 2
num_classes     = 51
input_size      = 416
graph           = tf.get_default_graph()
return_tensors  = utils.read_pb_return_tensors(graph, pb_file, return_elements)

# Face Detection ''
folder_path = '../Facenet/'
pkl_path = folder_path + 'contributed/myclassifer.pkl'
font_path = folder_path + 'contributed/font/gulim.ttf'
embedding_path = folder_path + 'contributed/embeddings.npy'
label_path = folder_path + 'contributed/labels.npy'
class_path = folder_path + 'contributed/class_names.npy'

# 스레드를 사용해서 영상 정보를 QObject로 받는 VideoViewer
# r 설정

class VideoViewer(QtCore.QObject):

    '''카메라 뷰어'''

    ''' 
        --------------------------------------------------
        웹캠 관련 설정 방법                               
        --------------------------------------------------
        counter_camera : 상품을 촬영                     
        face_camera : 구매자를 촬영
        
        초기 설정은 영상 파일 경로명을 입력받습니다.
        
        웹캠을 사용하려면 cv2.VideoCapture 메소드의 인자에 
        영상 파일의 경로명 대신 웹캠의 장치 번호를 지정해주세요.
        ex) cv2.VideoCapture(0)
            cv2.VideoCapture(1)
        --------------------------------------------------
    '''
    counter_camera = cv2.VideoCapture('../test_images/test_0.webm')
    face_camera = cv2.VideoCapture('../test_images/test_1.mp4')

    # 이미지를 잘 받았는지, 어떤 이미지인지를 반환하는 함수 read()를 사용하여 프레임을 카메라로부터 받아온다.
    ret, image = counter_camera.read()

    # 이미지의 높이, 너비를 shape로부터 받아옴
    height, width = image.shape[:2]

    half_h = int(height/2)
    half_w = int(width/2)

    name = None
    take_picture = False
    # 수신 신호

    # 이미지를 시그널로 보냄
    videoSignal = QtCore.pyqtSignal(QtGui.QImage)
    Mvideo_signal = QtCore.pyqtSignal(QtGui.QImage)
    id_signal = QtCore.pyqtSignal(list)
    user_id_signal = QtCore.pyqtSignal(str)
    picture_signal = QtCore.pyqtSignal()



    #---------------------------------------------- 전역 변수 설정 완료 --------------------

    def __init(self, parent=None):
        super(VideoViewer, self).__init__(parent)


    def takePicuture(self):
        self.take_picture = True

    def inputName(self, input_name):
        self.name = input_name

    def best_face_search(self, faces):
        # 최적의 차이는 0
        best_face_bb = [0, 0, 0, 0]
        best_distance = 10000
        have_face_name = True
        face_name = "Unknown"
        face_embedding = np.array
        have_face = None

        if faces is not None:
            for face in faces:
                face_bb = face.bounding_box.astype(int)

                # 카메라의 중앙에 가장 가까운 얼굴만을 검출

                # 박스의 중앙을 특정
                x = abs(face_bb[2] - face_bb[0])
                y = abs(face_bb[3] - face_bb[1])

                # 카메라의 중앙에서 얼마나 떨어져 있는가를 계산
                cal_x = abs(x - self.half_w)
                cal_y = abs(y - self.half_w)

                distance = math.sqrt(math.pow(cal_x, 2) + math.pow(cal_y, 2))

                # 가장 작은 거리를 저장
                if best_distance > distance:
                    best_distance = distance
                    best_face_bb = [face_bb[0], face_bb[1], face_bb[2], face_bb[3]]
                    face_name = face.name
                    face_embedding = face.embedding

            have_face = 1

        return best_face_bb, face_name, have_face, face_embedding


    def add_overlays(self, frame, best_face_bb, face_name, frame_rate, enroll, num_count):

        cv2.rectangle(frame,
                    (best_face_bb[0], best_face_bb[1]), (best_face_bb[2], best_face_bb[3]),
                    (0, 255, 0), 2)


        cv2.putText(frame, face_name, (best_face_bb[0], best_face_bb[3]),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),
                    thickness=2, lineType=2)

        if enroll:
            b, g, r, a = 0, 255, 0, 0
            fontpath = font_path
            font = ImageFont.truetype(fontpath, 30)
            frame_pil = Image.fromarray(frame)
            draw = ImageDraw.Draw(frame_pil)

            if num_count < 10:
                draw.text((10, 30), "카메라에 얼굴 정면을 보여주세요", font=font, fill=(b, g, r, a))
            elif num_count < 20:
                draw.text((10, 30), "고개를 왼쪽으로 돌려주세요", font=font, fill=(b, g, r, a))
            else:
                draw.text((10, 30), "고개를 오른쪽으로 돌려주세요", font=font, fill=(b, g, r, a))
            frame = np.array(frame_pil)
        else:
            cv2.putText(frame, str(frame_rate) + " fps", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),
                    thickness=2, lineType=2)
        return frame


    def face_add(self,face_embedding, num_count, name, frame, best_face_bb):

        emb_array = np.load(embedding_path)
        labels = np.load(label_path)
        class_names = np.load(class_path)

        # 이름 입력 받는 곳 제거 및 이름을 매개 변수로 받아오게 매개 변수 추가
        # if 문 제거 밑 face_embedding 변수를 매개 변수로 추가해서 face.embedding을 대체
        print("얼굴등록")
        if num_count == 0:  # 첫번째 unknown을 나올 경우 class_name이 필요하다. 그 이후로는 필요가 없음
            class_names = np.append(class_names, name)
            labels = np.append(labels, labels[np.argmax(labels)] + 1)
            np.save(class_path, class_names)

        if num_count == 5:
            save_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            x = best_face_bb[0]
            y = best_face_bb[1] -20

            if y<0:
                y = 0

            w = best_face_bb[2] - best_face_bb[0]
            h = best_face_bb[3] - best_face_bb[1]

            save_img = save_img[y:y+h, x:x+w]
            user_name = self.name

            cv2.imwrite('../user_image/' + user_name + '.png', save_img)

        else:
            labels = np.append(labels, labels[np.argmax(labels)])
        emb_array = np.vstack((emb_array, face_embedding))
        np.save(embedding_path, emb_array)
        np.save(label_path, labels)
        # np.save("class_names.npy",class_names)
        print("numpy 파일 세이브 완료")
        return True, num_count + 1

    def train_classifier(self):
        # npy 파일 불러오기(classifier를 학습하기 위해)
        emb_array = np.load(embedding_path)
        labels = np.load(label_path)
        class_names = np.load(class_path)

        model = SVC(kernel='linear', probability=True)
        model.fit(emb_array, labels)
        with open(pkl_path, 'wb') as outfile:
            pickle.dump((model, class_names), outfile)
        print('Saved classifier model to file "%s"' % pkl_path)

    def startVideo(self):
        global image

        face_add_signal = False

        frame_interval = 10  # Number of frames after which to run face detection
        fps_display_interval = 5  # seconds
        frame_rate = 0
        frame_count = 0

        # 얼굴 인식을 위한 객체설정
        face_recognition = face.Recognition()
        start_time = time.time()

        num_count = 0  # 얼굴 등록 시 10개 이미지만 저장되도록 하기 위한 변수
        enroll = False  # 얼굴 등록중인지 아닌지
        showing = 0

        run_video = True

        with tf.Session(graph=graph) as sess:
            while run_video:
                # 비디오가 참일때만
                # 얼굴 이미지
                ret, image = self.face_camera.read()
                #print(image)
                image = cv2.flip(image, 1)
                color_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                #-------------------------------------------------------------------

                # Check our current fps(5초당 프레임레이트를 계산한다)

                if (frame_count % frame_interval) == 0:
                    faces = face_recognition.identify(color_image, enroll)  # 웹캠에서 얼굴 탐지 및 인식을 시도를 함

                    best_face_bb, best_face_name, have_face, face_embedding = self.best_face_search(faces) # 화면 중앙에 가장 가까운 얼굴의 이름과 좌표를 저장
                    end_time = time.time()

                    if (end_time - start_time) > fps_display_interval:
                        frame_rate = int(frame_count / (end_time - start_time))
                        start_time = time.time()
                        frame_count = 0


                    # 얼굴이 인식되고 얼굴 등록시작 신호가 들어오면
                    if have_face is not None and self.name is not None:
                        enroll, num_count = self.face_add(face_embedding, num_count, self.name, color_image, best_face_bb)

                    if self.take_picture == True:
                        save_img = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)
                        x = best_face_bb[0]
                        y = best_face_bb[1] - 20

                        if y < 0:
                            y = 0

                        w = best_face_bb[2] - best_face_bb[0]
                        h = best_face_bb[3] - best_face_bb[1]

                        save_img = save_img[y:y + h, x:x + w]
                        user_name = best_face_name
                        cv2.imwrite('../user_image/' + user_name + '.png', save_img)
                        self.take_picture = False

                    # print(num_count)
                    if num_count == 30:
                        self.train_classifier()
                        num_count = 0
                        enroll = False
                        self.name = None

                add_frame = self.add_overlays(color_image, best_face_bb, best_face_name, frame_rate, enroll, num_count)
                #print(best_face_bb)
                self.user_id_signal.emit(best_face_name)

                frame_count += 1

                qt_image = QtGui.QImage(add_frame,
                                        self.width,
                                        self.height,
                                        color_image.strides[0],
                                        QtGui.QImage.Format_RGB888
                )

                # -------------------------------------------------------------------

                # 이미지를 비디오 시그널로 보낸다.
                self.videoSignal.emit(qt_image)

                #Object Detection
                counter_ret, counter_image = self.counter_camera.read()
                if counter_ret:
                    image = Image.fromarray(counter_image)
                else:
                    raise ValueError("No image!")
                frame_size = counter_image.shape[:2]
                image_data = utils.image_preporcess(np.copy(counter_image), [input_size, input_size])
                image_data = image_data[np.newaxis, ...]
                prev_time = time.time()
                counter_image = cv2.cvtColor(counter_image, cv2.COLOR_BGR2RGB)
                pred_sbbox, pred_mbbox, pred_lbbox = sess.run(
                    [return_tensors[1], return_tensors[2], return_tensors[3]],
                    feed_dict={return_tensors[0]: image_data})
                pred_bbox = np.concatenate([np.reshape(pred_sbbox, (-1, 5 + num_classes)),
                                            np.reshape(pred_mbbox, (-1, 5 + num_classes)),
                                            np.reshape(pred_lbbox, (-1, 5 + num_classes))], axis=0)
                bboxes = utils.postprocess_boxes(pred_bbox, frame_size, input_size, 0.3)
                bboxes = utils.nms(bboxes, 0.45, method='nms')
                class_id = []
                for i, bbox in enumerate(bboxes):
                    class_id.append(int(bbox[5]))

                image = utils.draw_bbox(counter_image, bboxes)
                curr_time = time.time()
                exec_time = curr_time - prev_time
                result = np.asarray(image)

                # 상품 이미지
                m_qt_image = QtGui.QImage(image,
                                        self.width,
                                        self.height,
                                        image.strides[0],
                                        QtGui.QImage.Format_RGB888
                                        )

                # 이미지를 비디오 시그널로 보낸다.
                self.Mvideo_signal.emit(m_qt_image)

                self.id_signal.emit(class_id)

                # 이벤트를 루프 시킨다.
                # 25ms 단위로 루프 결과를 가져온다.
                loop = QtCore.QEventLoop()
                QtCore.QTimer.singleShot(30, loop.quit)
                loop.exec_()
