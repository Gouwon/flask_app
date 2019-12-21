from flask import Blueprint
from flask import render_template, url_for, request, redirect, session, jsonify
from .models import User
from .init_db import db_session
from sqlalchemy import func



from pprint import pprint


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = {}
        for rq in request.form:
            key = rq
            value = request.form.get(rq)
            data[key] = value
        
        pprint(data)
        
        user = User(username=data["username"], userid=data["userid"], password=data["password1"], make_sha=True)
        try:
            db_session.add(user)
            db_session.commit()
        except SQLAlchemyError as sqlerr:
            db_session.rollback()
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login(next=None):
    if request.method == 'POST':
        data = {
            'id' : request.form.get('id'),
            'pw' : func.sha2(request.form.get('password'), 256)
        }

        pprint(data)
        # user = User.query.filter(User.userid==data['id'], User.password==data['pw']).first()
        user = User.query.filter(User.userid=='abc@efg.com', User.password=='a').first()
        if(user is not None):
            session['loginUser'] = user._jsonify()
            session['loginUser']['id'] = user.id    # user index를 클라이언트에 안 주기 위해서....
            res = jsonify(user._jsonify())
        return render_template('login.html', result="not found") if (user is None) else url_for(next)
    return render_template('login.html')

@bp.route('/logout', methods=['GET', 'POST'])
def logout():
    del(session)
    return url_for('root')

@bp.route('/help', methods=['GET', 'POST'])
def help():
    return render_template('help.html')