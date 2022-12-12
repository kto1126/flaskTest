from flask import Flask, Blueprint, request, render_template
from flask_googlemaps import GoogleMaps, Map,icons,get_address,get_coordinates
from socket import *
#
# # AF: 어드레스패밀리(주소체계) 인터넷용이니, 다른거써봐야암 ,SOCK: 소켓타입
# serverSock = socket(AF_INET, SOCK_STREAM)
#
# # 클라이언트 만들때 불필요함, 서버를 운용할때 반드시 필요
# serverSock.bind(('',8080)) # 생성된 소켓번호와 어드레스 패밀리를 연결해준느것
# #(ip, port) 인데 '' 인경우에는 INADDR_ANY를 의미(모든 인터페이스와 연결하고싶다면 빈 문자열을 넣는다.)
# # 브로드캐스트를 하고싶으면 ''도 입력하며됨
# # 따라서 8080번포트에서 모든 인터페이스에게 연결하도록하는 의미
#
# # 상대방의 접속을 기다리는 단계임
# # listen(1)는 소켓이 총 몇개의 동시 접속까지 허용할 것인가?
# # 1을 입력하면 단 한개 의 접속만을 허용할것이고, 인자를 입력하지않으면 자의적으로 판단해서 임의 숫자로 listen한다고 합니다.
# serverSock.listen(1)
#
# # 접속을수락하고, 그후에 통신하기위해서 accept를 사용해야함
# connectionSock,addr = serverSock.accept()
# print(str(addr), '에서 접속이 확인되었습니다.')
# # return값으로 새로운소켓과 상대방의 af를 전달받음
# data = connectionSock.recv(1024)
# print('받은 데이터 : ', data.decode('utf-8'))
#
# connectionSock.send('I am a server.'.encode('utf-8'))
# print('메시지를 보냈습니다.')

# #-----------여기까지 서버소켓-------------
# serverSock = socket(AF_INET, SOCK_STREAM)
# port = 8080
# serverSock.bind(('',port))
# serverSock.listen(1)
# print(f'{port}번 포트로 접속 대기중...')
#
# connectionSock, addr = serverSock.accept()
# print(str(addr),'에서 접속되었습니다.')
#
# while True:
#     sendData = input('>>>')
#     connectionSock.send(sendData.encode('utf-8'))
#
#     recvData = connectionSock.recv(1024)
#     print('상대방 :', recvData.decode('utf-8'))

# def send(sock):
#     sendData = input('>>>')
#     sock.send(sendData.encode('utf-8'))
#
#
# def receive(sock):
#     recvData = sock.recv(1024)
#     print('상대방 :', recvData.decode('utf-8'))
#
#
# port = 8080
# serverSock = socket(AF_INET, SOCK_STREAM)
# serverSock.bind(('', port))
# serverSock.listen(1)
#
# print(f'{port}번 포트로 접속대기중...')
#
# connectionSock, addr = serverSock.accept()
# print(str(addr), '에서 접속되었습니다.')
#
# while True:
#     send(connectionSock)
#     receive(connectionSock)

# 송수신순서 상관없이 동시적으로 할수있게 Thread(스레드) 기능 활용
# import threading
# def send(sock):
#     while True:
#         sendData = input('>>>')
#         sock.send(sendData.encode('utf-8'))
#
# def receive(sock):
#     while True:
#         recvData = sock.recv(1024)
#         print('상대방 :', recvData.decode('utf-8'))
#
# port = 8081
# serverSock = socket(AF_INET,SOCK_STREAM)
# serverSock.bind(('',port))
# serverSock.listen(1)
#
# print(f'{port}번 포트로 접속대기중...')
#
# connectionSock, addr = serverSock.accept()
#
# print(str(addr),'에서 접속되었습니다.')
#
# # target은 실제로 스레드가 실행할 함수를 입력, 그 함수에게 전달할 인자를 args에 입력
# sender = threading.Thread(target=send, args=(connectionSock,))
# receiver = threading.Thread(target=receive, args=(connectionSock,))
# # args에 인자가 하나하면은 튜플아니라 var식으로 입력으로 됀다.
# # 그래서 인자, 하면은 (var,)시그올 입력해야 튜플으로 인식이 된다.
#
#
# sender.start()
# receiver.start()
#
# import time
# while True:
#     time.sleep(1)
#     pass
#
#


"""
이거는 flask_googlemap 라이브러리에서 있는 gmapjs.html 있는데
수정 안하면 구글 맵 지도 아예 안뜬다. 따라서 수정해야한다.
임시적으로 메모장에다가 적을예정이니 참고하세요
"""



google = Blueprint('googleMap',__name__,'/googleMap')
# @kakao.route('/kakaoMap result', methods = ['POST','GET'])
# def kakaomap():
#     if request.method == 'POST':
#         result = request.form
#         return render_template("information/crackdown_inquiry.html",prediction = result)


# 이거는 나중에 에러가 뜨면은 area에 뭔가 잘못된 글자가 들어 있다는 뜻임
# 데이터베이스
datas = []
from module.dbmodule import Database
a = Database()
sql = "select * from tb_area_test"
row = a.executeAll(sql)

for i in row:
    print(i['regulation_area'])
    datas.append(i['regulation_area'])


print(datas)

print(datas[10:])

for i in datas[10:]:
    print(i)

print({sq for sq in datas[10:]})
# 주소텍스트에서 좌표 가져오기 테스트 완료
# API_KEy는 개인용키이므로 유출하지마셈
a = get_coordinates(API_KEY='AIzaSyBx6q68vuftoJ5VoCP6RjJotaUwlbNJADg',address_text=row[7]['regulation_area'])
print((a['lat'],a['lng'],'일곡동'))







# json 형태로 가져와야하나?
@google.route('/googleMap_api')
def googlemap():
    # 뷰에서 지도생성
    # 이거는 싱글 지도(기본 지도)임
    gmap = Map(
        identifier="gmap",
        varname="gmap",
        lat=35.149681,
        lng=126.919929,
        markers = [(35.149681,126.919929)],
        language="ko",
        style="height:600px;width:1100px;margin:0;",
    )
    test = []
    for r in row:
        print(r['regulation_area'])
        test.append(r['regulation_area'])
    final_test = []
    for j in test[10:]:
        result = get_coordinates(API_KEY='AIzaSyBx6q68vuftoJ5VoCP6RjJotaUwlbNJADg', address_text=j)
        final_result = (result['lat'],result['lng'],j)
        print(final_result)
        print(type(final_result))
        final_test.append(final_result)
    print(final_test)

    multimap = Map(
        identifier="multimap",
        varname="multimap",
        lat=35.149681,
        lng=126.919929,
        language="ko",
        markers={
            # icons.dots.green: [(35.149681,126.919929, "hello")],
            # icons.dots.blue: [(35.149681,126.919400, "hi!")],
            icons.dots.blue: [sq for sq in final_test]
        },
        style="height:600px;width:1100px;margin:0;",
    )

    return render_template("information/crackdown_inquiry.html",gmap=gmap,multimap=multimap,test=test)
# import flask_googlemaps
# flask_googlemaps.GoogleMaps(key="AIzaSyCLZi8Qe4emYzsFiDu49sSZB_jdGQei7yA")

print((35.149681,126.919929, "hello"))
# print(sq for sq in final_test)
#
import googlemaps
import folium
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from datetime import datetime








# 지오코딩맵 코드임
# gmaps = googlemaps.Client(key='AIzaSyASdVaMqpJL4AQxRB7x4VMegCCUnvfN74k')
# geocde_result = gmaps.geocode('서울영등포경찰서',language="ko")
# print(geocde_result)
# print(geocde_result[0]['address_components'])
# print(geocde_result[0]['formatted_address'])
#
# reverse_geocode_result = gmaps.reverse_geocode((37.5260441,126.9008091),language="ko")
# print(reverse_geocode_result)
# a = folium.Map(location=[37.5260441,126.9008091])
# print(f"folium Vesrion: {folium.__version__}")
#
# #위도, 경도
# lat, lon = 37.504811111562, 127.025492036104
# # 줌 크기
# zoom_size = 12
#
# #구글 지도 타일 설정
# tiles = "http://mt0.google.com/vt/lyrs=m&h1=ko&x={x}&y={y}&z={z}"
# # 속성 설정
# attr = "Google"
# # 지도 객체 생성
# m = folium.Map(location=[lat,lon],
#                zoom_start= zoom_size,
#                tiles = tiles,
#                attr = attr)
# m
