from flask import Blueprint
from flask import render_template, url_for, request, redirect, session, jsonify
from .models import User
from functools import wraps

from pprint import pprint


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/regist', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = {}
        # QQQ adding user to db
        for rq in request.form:
            key = rq
            value = request.form.get(rq)
            data = {key : value}
        pprint(data)
        return redirect(url_for('auth.login'))
    return render_template('regist.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = {
            'id' : request.form.get('id'),
            'pw' : request.form.get('pw')
        }
        # QQQ userid, password 입력값으로 치환하기.
        user = User.query.filter(User.userid=='abc@efg.com', User.password=='a').first()
        if(user is not None):
            session['loginUser'] = user._jsonify()
            res = jsonify(user._jsonify())
        return render_template('login.html', result="not found") if (user is None) else res
    return render_template('login.html')

