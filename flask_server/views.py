from flask_server import app
from functools import wraps
from flask import render_template, jsonify, url_for, redirect, request


users = [ {"id" : 1, "name" : "김일수"}, {"id" : 2, "name" : "김이수"} ]

@app.route('/test', methods=['GET'])
def draw_test():
    return render_template('test.html')

@app.route('/users/', methods=['GET'])
def get_users():
    return jsonify({"result" : users})

@app.route('/users/', methods=['POST'])
def take_users():
    way = request.form.get('method')

    if way == "POST":
        return redirect(url_for('create_users'), code=307)
    elif way == "PUT":
        return redirect(url_for('update_users'), code=307)
    else:
        return redirect(url_for('delete_users'), code=307)

@app.route('/users/c', methods=['POST'])
def create_users():
    return jsonify({"result":"this is POST method"})

@app.route('/users/u', methods=['POST'])
def update_users():
    return jsonify({"result":"this is PUT method"})

@app.route('/users/d', methods=['POST'])
def delete_users():
    return jsonify({"result":"this is DELETE method"})