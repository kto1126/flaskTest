from flask import Blueprint, request, render_template, flash, redirect, url_for
#from flask import current_app as ap


main = Blueprint('main',__name__,url_prefix='/')

@main.route('/')
def index():
    return render_template("main_content.html")

@main.route('/login')
def login():
    return render_template("manager/login.html")

@main.route('/signup')
def sigup():
    return render_template("manager/sigup.html")

@main.route('/features')
def features():
    return render_template("area/features.html")

@main.route('/car collection')
def car_collection():
    return render_template("information/car_collection.html")


@main.route('/save')
def save():
    return render_template("information/save.html")


@main.route('/crackdown inquiry')
def crackdown_inquiry():
    return render_template("information/crackdown_inquiry.html")


@main.route('/drones Registration and operation')
def Registration_and_operation():
    return render_template("drones/Registration_and_operation.html")
# @main.route('/login_select_query', methods = ['POST', 'GET'])
# def login_select_query():
#     id = request.form['sigup_id']
#     password = request.form['sigup_pw']
#     drone_name = request.form['sigup_droneName']
#     if id == 'test' and password == '1234' and drone_name == 'tello':
#         print(id,password,drone_name)
#         return redirect(url_for('main.login'))
#     else:
#         return redirect(url_for('main.index'))
    # queery = dbmodule.Database.executeAll("select * from test where id = % s",(id,))
    # print(queery)
