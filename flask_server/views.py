from flask_server import app
from functools import wraps
from flask import render_template, jsonify, url_for, redirect, request, session
from flask_server.models import User

@app.route('/', methods=['GET'])
def template_base():
    return render_template('base.html')


@app.route('/test', methods=['GET'])
def draw_test():
    return render_template('test.html')
    # return redirect('https://www.naver.com')

# 대문 페이지
@app.route('/cover', methods=['GET'])
def template_cover():
    return render_template('cover.html')

# 로그인 페이지
@app.route('/login', methods=['GET'])
def template_login():
    return render_template('login.html')

# 가입 페이지
@app.route('/join', methods=['GET'])
def template_join():
    return render_template('join.html')

@app.route('/login', methods=['POST'])
def login():

    data = request.form
    email = data['email']
    passwd = data['passwd']
    
    user = User.query.filter(email==email, passwd==passwd).one()
    print("<<<<<<<<", user)

    if user != None:
        session['loginUser'] = {'userid': user.id, 'nickname': user.nickname}
        if next != None:
            return redirect(next)
        else:
            return redirect('/main')
    

    return redirect('/login')


# 개인정보수정 페이지
@app.route('/setup', methods=['GET'])
def template_setup():
    return render_template('set_up.html')

# 포스트문서 조회 페이지
@app.route('/read', methods=['GET'])
def template_post():
    return render_template('post.html')

# 포스트문서 등록 페이지
@app.route('/add', methods=['GET'])
def template_post_add():
    return render_template('post_add.html')

# 포스트문서 수정 페이지
@app.route('/modify', methods=['GET'])
def template_post_modify():
    return render_template('post_modify.html')

# 문서목록 조회 페이지
@app.route('/inquiry', methods=['GET'])
def template_list_inquiry():
    return render_template('list_inquiry.html')

# 메인 페이지
@app.route('/main', methods=['GET'])
def template_main():
    return render_template('main.html')

@app.route('/tt', methods=['GET'])
def template_txteditor():
    return render_template('txteditor.html')
