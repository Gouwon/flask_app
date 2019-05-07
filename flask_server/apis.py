from flask_server import app
from functools import wraps # login required annotaion!
from flask import Flask, render_template, jsonify, url_for, redirect, request, session

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
from flask_server.models import User, Post
from flask_server.init_db import db_session

from pprint import pprint


users = [ {"id" : 1, "name" : "김일수"}, {"id" : 2, "name" : "김이수"} ]

# 로그인 API
@app.route('/users', methods=['GET'])
def get_users():
    '''
        :: returns all user list in json.
    '''

    user_list = User.query.all()
    user_list = [user.get_json() for user in user_list]
    
    return jsonify({"result" : user_list})


@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    '''
        :: returns specific user information. if not found, then returns none.
    '''

    user = User.query.filter_by(id=user_id).first()
    result = user.get_json()
    
    if result == "":
        return jsonify({"result" : "there is no such user."}) 

    return jsonify(result)


@app.route('/users/<user_id>', methods=['POST'])
def take_user(user_id):
    way = request.form.get('method')

    if way == "PUT":
        return redirect(url_for('update_user'), code=307)
    else:
        return redirect(url_for('delete_user'), code=307)

@app.route('/users/', methods=['POST'])
def create_user():
    '''
        :: add new user to User table using request.form json data.
        if success, return code 200.
    '''

    jsonData = request.get_json()
    data = jsonData['data']
    email = data['email']
    passwd = data['passwd']
    nickname = data['nickname']
    # print(">>>>>> ", data, type(data), data['methods'])
    
    # QQQ 기가입자인지 확인이 필요함.
    # user_list = url_for('get_users')
    # for ujson in user_list:
    #     if ujson['email'] == email:
    #         return jsonify({"result" : {"code" : 500, "message" : "already joined user."}})
    #         break

    try:
        u = User(email, passwd, nickname, make_sha=True)
        db_session.add(u)
        db_session.commit()
        return jsonify({"result" : {"code" : 200, "message" : "user successfully added."}})
    except SQLAlchemyError as sqlerr:
        db_session.rollback()
        return jsonify({"result" : {"code" : 500, "message" : "user add failed."}})
    


@app.route('/users/u/<user_id>', methods=['POST'])
def update_user(user_id):
    '''
        :: update selected user.
    '''

    jsonData = request.get_json()
    data = jsonData['data']
    data['passwd'] = func.sha2(data['passwd'], 256)

    try:
        User.query.filter_by(id=user_id).update(data, synchronize_session=False)
        db_session.commit()
        return jsonify({"result" : {"code" : 200, "message" : "user successfully updated."}})
    except SQLAlchemyError as sqlerr:
        db_session.rollback()
        return jsonify({"result" : {"code" : 500, "message" : "user is existed."}})

@app.route('/users/d/<user_id>', methods=['POST'])
def delete_user(user_id):
    '''
        :: delete selected user.
    '''

    try:
        User.query.filter_by(id=user_id).delete()
        db_session.commit()
        return jsonify({"result" : {"code" : 200, "message" : "user successfully deleted."}})
    except SQLAlchemyError as sqlerr:
        db_session.rollback()
        return jsonify({"result" : {"code" : 500, "message" : "user is existed."}})


# POST API
@app.route('/posts/add', methods=['POST'])
def post_add():

    # text editor head & content
    head = request.form.get('head')
    content = request.form.get('content')
    # author = session['loginUser']['id']
    author = 1
    print("0")
    # return jsonify({'result':'OK'})
    post = Post(head, content, author)
    print(">>>>>>", post)
    try:
        print("1")
        db_session.add(post)
        print("2")
        db_session.commit()
        print("3")
        return jsonify({"result" : {"code" : 200, "message" : "post successfully added."}})
    except SQLAlchemyError as sqlerr:
        print("4")
        db_session.rollback()
        print("5")
        return jsonify({"result" : {"code" : 500, "message" : "post is failed to add."}})