from flask import Blueprint,url_for,request,render_template,flash,session,g, redirect
from module import dbmodule

# 데이터베이스 추가해야할 함수 써야할듯

logins = Blueprint('singup',__name__,url_prefix='/singup')
#static_folder='static',static_url_path='/static/css' 혹시나몰라서 남김

# 데이터베이스 없이 로그인 되는지 시험하는중
# @login.route('/login_select_query')
# def login_select_query():
#     id = request.form['id']
#     password = request.form['pw']
#     drone_name = request.form['drone_name']
#     if id == 'test' and password == '1234' and drone_name == 'tello':
#         print(id,password,drone_name)
#         return redirect(url_for('login'))
#     else:
#         return redirect(url_for('index'))
#     queery = dbmodule.Database.executeAll("select * from test where id = % s",(id,))
#     print(queery)
#

# 임시적으로 회원가입 했음
# 만약 정식 회원가입 할 경우에는 할예정
# id, pw , drone_name 테스트 완료
# 이제 데이터베이스 연결해가지고 해야함
# 데이터베이스 입력 집어넣은거 테스트 완료
# 데이터베이스 아이디있으면 이미있는 아이디 반환
# 없으면 환영합니다 반환 이것을 js로 바꾸면됨
@logins.route('/login_singup_query',methods= ['GET','POST'])
def login_singup_query():
    if request.method == 'POST':
        welcome = ''
        No_welcome = ''
        id = request.form['sigup_id']
        password = request.form['sigup_pw']
        drone_name = request.form['sigup_droneName']
        db_class = dbmodule.Database()
        # query = f"insert into test values ({id},{password},{drone_name})"
        # db_class.execute(query)
        # db_class.commit()
        query1 = f"select id from test where id = '{id}'"
        print(query1)
        query2 = f"insert into test values ({id},{password},{drone_name})"
        print(query2)
        row1 = db_class.executeOne(query1)
        print(row1)
        print(type(row1))
        if row1 is None:
            welcome = '회원가입 완료되었습니다'
            query = f"insert into test values ('{id}','{password}','{drone_name}')"
            db_class.execute(query)
            db_class.commit()
            return render_template("manager/login.html", welcome=welcome)
        elif row1['id'] == id:
            if row1['id'] == '':
                No_welcome='가입할 아이디랑 비밀번호 입력하시오'
                return render_template("manager/sigup.html", No_welcome = No_welcome)
            else:
                No_welcome = '이미 있는 아이디입니다. 다시 회원가입 하세요'
                return render_template("manager/sigup.html", No_welcome = No_welcome)
        # else:
        #     welcome = '회원가입 완료되었습니다'
        #     query = f"insert into test values ('{id}','{password}','{drone_name}')"
        #     db_class.execute(query)
        #     db_class.commit()
        #     return render_template("manager/login.html", welcome = welcome)

    #
    # if id == 'test' and password == '1234' and drone_name == 'tello':
    #     print(id,password,drone_name)
    #     return redirect(url_for('main.login'))
    # else:
    #     return redirect(url_for('main.index'))

# 로그인
# 테스트완료
# 이제는 데이터베이스 연결해가지고 해야함
# 데이터베이스 연결성공, 테스트완료


# 임시 테스트한것
@logins.route('/login_check')
def login_check():
    return render_template('home_test.html',id=session['id'])



@logins.route('/login_test',methods= ['GET','POST'])
def login_test():
    msg = ''
    if request.method == 'POST':
        id = request.form['id']
        pw = request.form['pw']
        db_class = dbmodule.Database()
        sql = f"select * from test where id = '{id}'and password = '{pw}'"
        print(sql)
        row = db_class.executeAll(sql)
        row1 = db_class.executeOne(sql)
        row2 = db_class.execute(sql)

        print(row)
        print(row1)
        print(row2)
        if row1:
            if row1['id'] == '' and row1['password'] == '':
                msg = '로그인 아이디랑 비밀번호 입력하세요!'
                return render_template('manager/login.html',msg=msg)
            else:
                session['loggedin'] = True
                session['id'] = row1['id']
                session['pw'] = row1['password']
                # return redirect(url_for('singup.login_check'))
                return redirect(url_for('main.mains'))
        else:
            msg = '아이디 틀렸거나 비번 다시 하세요'
    return render_template('manager/login.html',msg=msg)

        #
        # if id == row1['id'] and pw == row1['password']:
        #     return redirect(url_for('main.index')) # 로그아웃 만들어야함
        # else:
        #     return "로그인 실패!"

@logins.route('/logout')
def logout():
    session.pop('loggedin',None)
    session.pop('id',None)
    return redirect(url_for('main.index'))