from flask import Blueprint
from flask import render_template, url_for, request, redirect
from .models import User

from pprint import pprint

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/regist', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        for rq in request.form:
            print(rq, " || ", request.form.get(rq))
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
        user = User.query.filter(User.userid=='abc@efg.com', User.password=='s').first()
        return render_template('login.html', result="not found") if (user is None) else redirect(url_for('root'))
    return render_template('login.html')