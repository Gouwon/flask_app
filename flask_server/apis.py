from flask_server import app
from functools import wraps # login required annotaion!
from flask import Flask, render_template, jsonify, url_for, redirect, request, session, send_from_directory
from werkzeug.utils import secure_filename  # this is required for file upload from client

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
from flask_server.models import User, Post
from flask_server.init_db import db_session

from pprint import pprint
import os

users = [ {"id" : 1, "name" : "김일수"}, {"id" : 2, "name" : "김이수"} ]

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
    post = Post(head, content, author)
    try:
        db_session.add(post)
        db_session.commit()
        return jsonify({"result" : {"code" : 200, "message" : "post successfully added."}})
    except SQLAlchemyError as sqlerr:
        db_session.rollback()
        return jsonify({"result" : {"code" : 500, "message" : "post is failed to add."}})

@app.route('/files', methods=['POST'])
def take_file(user_id):
    way = request.form.get('method')

    if way == "POST":
        return redirect(url_for('upload_file'), code=307)
    else:
        return redirect(url_for('delete_file'), code=307)

# image uploade api

@app.route('/files/upload', methods=['POST'])
def upload_file():
    '''
        :: returns img src string as json.
        :: if there is same name file in server, then it will automactically rename the file.
        :: when server do this, server store actual file in directory which is made for each user, and insert file information(filename, filename2, size, user, datatype...) into db so that server can determine user's total usage to restrict him/her upload.
    '''


    ## user directory check (if not found on server, then create specific user's directory)
    # user_id = session['login']['userid']
    user_id = 1

    
    user_directory_path = app.config['UPLOAD_FOLDER'] + str(user_id)
    _isdir = os.path.isdir(user_directory_path)

    if not(_isdir):
        os.mkdir(user_directory_path)
    
    ## save uploaded file in user directory
    upfile = request.files['file']

    print(upfile)
    return jsonify({"result" : "OK"})
    invalid_character_list = ['"', '\\', '|', '/', '*', '?', '<', '>', ':']
    
    filename = str(upfile.filename)
    for invalid_character in invalid_character_list:
        filename.replace(invalid_character, "")

    user_file = os.path.join(user_directory_path, filename)
    if file and allowed_file(filename):
        if os.path.isfile(user_file):
            idx = user_file.rindex('.')
            if idx == -1:
                user_file += '1'
            else:
                user_file = user_file[:idx] + '1' + user_file[idx:]
        file.save(user_file)

    ## insert file information into db


    ## return file src in string as json formatting

    return jsonify({"filepath" : user_file[43:] })

@app.route('/files/delete/<filename>', methods=['POST'])
def delete_file():
    return jsonify({"result" : "OK"})