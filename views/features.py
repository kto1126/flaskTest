from flask import Blueprint, redirect, flash, Flask,url_for,request,render_template, Response
from socket import *
import cv2
import os
import datetime
from module.tello_module import Tello

video_camera = None
global_frame = None
camera_frame = None
tello = None
tello = Tello()

# FPS
FPS = 25


# #세션 생성해주는것보이니까 굳이 필요없을것같네? 폴더 생기는것
# if True:
#     ddir = "../Sessions"
#
#     if not os.path.isdir(ddir):
#         os.mkdir(ddir)
#
#     # :를 -로 바꿔야함
#     ddir = "../Sessions/Session {}".format(str(datetime.datetime.now())[0:19].replace(':','-'))
#     os.mkdir(ddir)

# 실시간 영상 찍을수있는 함수
def video_stream():
    content = ''
    global video_camera
    global global_frame
    global camera_frame

    if video_camera == None:
        video_camera = tello
        if not video_camera.connect():
            content = '텔로 연결 하십시오'
            print(content)
            return
        if not video_camera.set_speed(10):
            content = '속도를 가능한 낮게 설정하지 마십시오.'
            print(content)
            return
        if not video_camera.streamoff():
            content = '비디오 끄지 않았습니다.'
            print(content)
            return
        if not video_camera.streamon():
            content = '비디오 시작하지 않았습니다.'
            print(content)
            return

    while True:
        frame_read = video_camera.get_frame_read()

        should_stop = False
        video_camera.get_battery()

        if True:
            print("디버그모드 활성화함")
        while not should_stop:
            if frame_read.stopped:
                frame_read.stop()
                break

            ori_frame = frame_read.frame
            frame = ori_frame
            if ori_frame.any():
                success, jpeg = cv2.imencode('.jpg',ori_frame)
                if success:
                    frame = jpeg.tobytes()

            if frame != None:
                global_frame = frame
                yield (b'--frame\r\n'b'Conetent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
            else:
                yield (b'--frame\r\n'b'Conetent-Type: image/jpeg\r\n\r\n' + global_frame + b'\r\n\r\n')


#영상 프레임 얻게하는것
@staticmethod
def get_frame(self):
    ret, frame = self.cap.read()

    if ret:
        ret, jpeg = cv2.imenocde('.jpg',frame)

        if self.is_record:
            if self.out == None:
                fourcc = cv2.VideoWriter_fourcc(*'MJPG')
                self.out = cv2.VideoWriter('./static/video.avi',fourcc,20.0,(640,480))
            ret,frame = self.cap.read()
            if ret:
                self.out.write(frame)
        else:
            if self.out != None:
                self.out.release()
                self.out = None

        return jpeg.tobytes()


features = Blueprint('features',__name__,url_prefix='/features')


# 실시간 영상
@features.route('/video_feed')
def video_feed():
    return Response(video_stream(),mimetype="multipart/x-mixed-replace; boundary=frame")

@features.route('/takeOff')
def takeOff():
    drone_terbang = tello
    drone_state = 'Drone Takeoff'
    if not drone_terbang.takeoff():
        print(drone_state)
        return render_template("area/features.html",drone_state=drone_state)
    return render_template("area/features.html")

@features.route('/Land')
def Land():
    drone_terbang = tello
    drone_state = 'Drone Landing'
    if not drone_terbang.land():
        print(drone_state)
        return render_template("area/features.html",drone_state=drone_state)
    return render_template("area/features.html")

@features.route('/Right')
def Right():
    drone_terbang = tello
    drone_state = 'Drone move right'
    if not drone_terbang.move_right(100):
        print(drone_state)
        return render_template("area/features.html",drone_state=drone_state)
    return render_template("area/features.html")
@features.route('/Left')
def Left():
    drone_terbang = tello
    drone_state = 'Drone move left'
    if not drone_terbang.move_left(100):
        print(drone_state)
        return render_template("area/features.html",drone_state=drone_state)
    return render_template("area/features.html")

@features.route('/forward')
def Forward():
    drone_terbang = tello
    drone_state = 'Drone move forward'
    if not drone_terbang.move_forward(100):
        print(drone_state)
        return render_template("area/features.html",drone_state=drone_state)
    return render_template("area/features.html")

@features.route('/back')
def Back():
    drone_terbange = tello
    drone_state = 'Drone move back'
    if not drone_terbange.move_back(100):
        print(drone_state)
        return render_template("area/features.html",drone_state=drone_state)
    return render_template("area/features.html")


@features.route('/cw')
def Rotate_clockwise():
    drone_terbange = tello
    drone_state = 'Drone rotate_clockwise'
    if not drone_terbange.rotate_clockwise(100):
        print(drone_state)
        return render_template("area/features.html",drone_state=drone_state)
    return render_template("area/features.html")

@features.route('/ccw')
def Rotate_counter_clockwise():
    drone_terbange = tello
    drone_state = 'Drone rotate_counter_clockwise'
    if not drone_terbange.rotate_counter_clockwise(100):
        print(drone_state)
        return render_template("area/features.html", drone_state=drone_state)
    return render_template("area/features.html")


@features.route('/flip')
def Flip():
    drone_terbange = tello
    drone_state = 'Drone flip'
    if not drone_terbange.flip("l"):
        print(drone_state)
        return render_template("area/features.html", drone_state=drone_state)
    return render_template("area/features.html")

@features.route('/flip_left')
def Flip_left():
    drone_terbange = tello
    drone_state = 'Drone move flip_left'
    if not drone_terbange.flip_left():
        print(drone_state)
        return render_template("area/features.html", drone_state=drone_state)
    return render_template("area/features.html")


@features.route('/flip_right')
def Flip_right():
    drone_terbange = tello
    drone_state = 'Drone move flip_right'
    if not drone_terbange.flip_right():
        print(drone_state)
        return render_template("area/features.html", drone_state=drone_state)
    return render_template("area/features.html")

@features.route('/flip_forward')
def Flip_forward():
    drone_terbange = tello
    drone_state = 'Drone move flip_forward'
    if not drone_terbange.flip_forward():
        print(drone_state)
        return render_template("area/features.html", drone_state=drone_state)
    return render_template("area/features.html")
@features.route('/flip_back')
def Flip_back():
    drone_terbange = tello
    drone_state = 'Drone move flip_back'
    if not drone_terbange.flip_back():
        print(drone_state)
        return render_template("area/features.html", drone_state=drone_state)
    return render_template("area/features.html")




