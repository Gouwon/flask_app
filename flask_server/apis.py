from flask_server import app
from functools import wraps # login required annotaion!
from flask import Flask, render_template, jsonify, url_for, redirect, request

from sqlalchemy.exc import SQLAlchemyError
from flask_server.models import User


users = [ {"id" : 1, "name" : "김일수"}, {"id" : 2, "name" : "김이수"} ]

# Test API


# 로그인 API
@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    '''
        :: returns specific user information. if not found, then returns none.
    '''

    user = User.query.filter_by(id=user_id).first()
    result = user.get_json()
    # result = {"id" : 1, "name" : "김일수"}
    
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
    data = request.is_json
    
    
    
    print(">>>>>> ", data, type(data))
    # data1 = request.get_json()
    # print(">>>>>> ", data1, type(data1))
    # QQQ 기가입자인지 확인이 필요함.
    # u = url_for('/get_user')

    # if "id" not in u.keys():
    try:
        print("add new user to User table using request.form json data")
        print("%(email)s, %(password)s, %(nickname)s" % data)
        u = User("%(email)s, %(password)s, %(nickname)s", make_sha=True) % data
        db_session.add(u)
        db_session.commit()
        return jsonify({"result" : {"code" : 200, "message" : "user successfully added."}})
    except SQLAlchemyError as sqlerr:
        db_session.rollback()

    # return jsonify({"result":"this is POST method"})
    return jsonify({"result" : {"code" : 500, "message" : "user is existed."}})

@app.route('/users/u/<user_id>', methods=['POST'])
def update_user(user_id):
    '''
        :: update selected user.
    '''

    data = {}

    u = url_for('/get_user', user_id=user_id)

    if "id" not in u.keys():
        try:
            User.query.filter_by(id=user_id).update(data, synchronize_session=False)
            db_session.commmit()
        except SQLAlchemyError as sqlerr:
            db_session.rollback()
        return jsonify({"result" : {"code" : 200, "message" : "user successfully updated."}})

    # return jsonify({"result":"this is PUT method"})
    return jsonify({"result" : {"code" : 500, "message" : "user is existed."}})

@app.route('/users/d/<user_id>', methods=['POST'])
def delete_user(user_id):
    '''
        :: delete selected user.
    '''
    u = url_for('/get_user', user_id=user_id)
    if "id" not in u.keys():
        try:
            User.query.filter_by(id=user_id).delete()
            db_session.commit()
        except SQLAlchemyError as sqlerr:
            db_session.rollback()
        return jsonify({"result" : {"code" : 200, "message" : "user successfully deleted."}})

    # return jsonify({"result":"this is PUT method"})
    return jsonify({"result" : {"code" : 500, "message" : "user is existed."}})