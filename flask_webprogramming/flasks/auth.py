from flask import Blueprint
from flask import render_template, url_for, request, redirect, session, jsonify
from sqlalchemy import func
from .models import User
from .init_db import db_session
from .validators import RegistrationForm

from pprint import pprint


bp = Blueprint('auth', __name__, url_prefix='/auth')

# C R U D

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    # QQQQQ form validator 완료하기.
    if request.method == 'POST':
        data = {}
        try:
            print(">>>>> form.validate(), ", form.validate())
            print("\n>>>>> form.data ", form.data)
            print("\n>>>>> form.errors ", form.errors)
            for i in form.data:
                print("\n>>>>> form.data[%s]" % i, form.data[i])
        except Exception as err:
            print(">>>>> form.validate() err ", err)
        
        return "OK"

        for rq in request.form:
            key = rq
            value = request.form.get(rq)
            data[key] = value
        
        user = User(username=data["username"], userid=data["userid"], \
                    password=data["password1"], make_sha=True)
        try:
            db_session.add(user)
            db_session.commit()
        except SQLAlchemyError as sqlerr:
            db_session.rollback()
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login(next=None):    
    next = request.args.get('next') if request.args.get('next') is not None \
            else 'index'

    if request.method == 'POST':
        data = {
            'id' : request.form.get('id'),
            'pw' : func.sha2(request.form.get('password'), 256)
        }

        # user = User.query.filter(User.userid==data['id'], \
        #                          User.password==data['pw']).first()
        user = User.query.filter(User.userid=='abc@efg.com', \
                                User.password=='a').first()
        if(user is not None):
            session['loginUser'] = user._jsonify()
            res = jsonify(user._jsonify())
        return render_template('login.html', result="not found") \
                if (user is None) else redirect(url_for('bd.draw_board'))
    return render_template('login.html', next=next)

@bp.route('/logout', methods=['GET', 'POST'])
def logout():
    del(session)
    return url_for('root')

@bp.route('/help', methods=['GET', 'POST'])
def help():
    return render_template('help.html')