import os
from flask import Blueprint, Flask, render_template, request
from module.dbmodule import Database

# 파일경로 없을경우 경로생성
# if True:
#     ddir = "parking"
#     num_ddir = "numPlate"
#     if not os.path.isdir('../static/'+ddir):
#         os.mkdir('../static/' + ddir)
#     if not os.path.isdir('../static/'+num_ddir):
#         os.mkdir('../static/' + num_ddir)


car_num_saveView = Blueprint('car_num_saveView',__name__,url_prefix='/car_num_saveView')

maria = Database()
query = "select * from tb_area_test where regulation_date = '2022-12-07'"
row = maria.executeOne(query)
print(row)
print(row['imgdir_parking1'])
print(row['imgdir_parking2'])
print(row['imgdir_numplate'])

print(row['imgdir_parking1'][19:])
print(row['imgdir_parking1'][10:])
print(row['imgdir_numplate'][10:])

# data_list = []
#
# for i in row:
#     print(i)

# for a in row:
#     print(a)
#     data_dic = {
#         'imgidr_parking1': a[4]
#     }
#     data_list.append(data_dic)
# print(data_list)
@car_num_saveView.route('/saveView')
def car_saveView():
    # date = request.form['date']
    # # print(date)
    # maria = Database()
    # # 만약 날짜선택한다면 그나마 맞겠다싶음
    # query = "select * from tb_area_test where regulation_date = '2022-12-07'"
    # row = maria.executeOne(query)
    # # 그리고 날짜선택하고난뒤에 여러이미지 있으면은 for문으로 돌려야함
    # parking = row['imgdir_parking1'][10:]
    # numplate = row['imgdir_numplate'][10:]
    #, parking = parking, numplate = numplate
    return render_template("./information/save.html")

@car_num_saveView.route('/dateQuery',methods = ["GET","POST"])
def car_dateQuery():
    date = request.form['date']
    print(date)
    maria = Database()
    query = f"select * from tb_area_test where regulation_date = '{date}'"
    row = maria.executeAll(query)
    print(query)
    print(row)
    data_list = []
    for r in row:
        print(r)
        data_dic = {
            'parking': r['imgdir_parking2'][10:],
            'numplate': r['imgdir_numplate'][10:]
        }
        data_list.append(data_dic)
    print(data_list)
    return render_template("./information/save.html", data_list= data_list)