from flask import Blueprint
from flask import render_template, make_response, jsonify, request, session, redirect, url_for
from jinja2 import Markup
from .utils import _jsonify
from .models import Post
from .init_db import db_session
from sqlalchemy import desc
import json

from pprint import pprint


bp = Blueprint('bd', __name__, url_prefix='/board')

# board.html drwaing
@bp.route('/')
def draw_board():
    rs = Markup("<h1>this is test for striptags filter in jinja</h1>")
    r = { "rs" : rs }
    # r = _jsonify(r)
    return render_template('board.html', rs=r)

# reading board
@bp.route('/board_read')
@_jsonify
def board_read():
    # QQQ 작업 필요....
    # 제목, 글쓴이, 순서(등록/수정), 태그, 내용, 조건검색(날짜, startday-endday, 포스트 검색 보여줄 결과 수)
    # if query param is none, select limit 50
    args  = request.args
    if len(args) == 0:
        posts =  Post.query.filter().order_by(desc(Post.registdt)).limit(50)
    
    
    print("?????? ", args)
    print("args.items()args.items()args.items()args.items() ", args.items())
    print(",,,,,,,,,,,,,,,,,,,,,", args.to_dict(False))
    v = args.to_dict(flat=False)
    print("%(s)s %(v)s %(c)s" % v, type(v))

    for a in args.items():
        print("/////// ", a)


    for c in args.keys():
        print(c)
    # posts = [post._jsonify() for post in posts]

    # return posts
    return "OK"

@bp.route('/post_write')
@bp.route('/post_write/<str:method>/<int:postno>')
def post_write(method='GET', postno=None):
    if method != "GET":
        post = url_for("post_read", postno)
    # escape 문제 해결해야 함.
    result = { "result" : post }
    return render_template('write.html', result=result)

@bp.route('/post_create', method=['POST'])
@_jsonify
def post_create():
    # data = request.args.to_dict(flat=False) param
    received_data = request.get_json()
    input_data = received_data['data']

    post = Post(head=input_data['head'], content=input_data['content'], author=session['loginUser']['id'])

    try:
        db_session.add(post)
        db_session.commit()
        msg = "success"
    except Exception as sqlerr:
        db_session.rollback()
        print(">>>>> sqlerr ", sqlerr)
        msg = "failed"
    return { "result" : msg }

@bp.route('/post_read/<int:postno>')
@_jsonify
def post_read(postno):
    post = Post.query.filter(Post.id == postno).first()
    if post in None:
        return { "result" : "not Found" }
    return post

@bp.route('/post_update/<int:postno>')
@_jsonify
def post_update():
    post = url_for('post_read', postno)
    received_data = request.get_json()
    input_data = received_data['data']
    post.head = input_data['head']
    post.content = input_data['content']
    post.updatedt = post.setupdatedt()

    try:
        db_session.add(post)
        db_session.commit()
        msg = "success"
    except Exception as sqlerr:
        db_session.rollback()
        print(">>>>> sqlerr ", sqlerr)
        msg = "failed"    
    return { "result" : msg } 

@bp.route('/post_delete/<int:postno>')
@_jsonify
def post_delete():
    post = url_for('post_read', postno)
    try:
        db_session.delete(post)
        db_session.commit()
        msg = "success"
    except Exception as sqlerr:
        db_session.rollback()
        print(">>>>> sqlerr ", sqlerr)
        msg = "failed"
    return { "result" : msg }