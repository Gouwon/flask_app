from flask import Blueprint, render_template, make_response, jsonify, request, session, redirect, url_for, Response
from jinja2 import Markup
from sqlalchemy import desc
from .models import Post
from .init_db import db_session
import json
from .decorators import login_required, _jsonify
from .utils import string_to_dict

from pprint import pprint


bp = Blueprint('bd', __name__, url_prefix='/board')

# board.html drwaing
# reading board
@bp.route('/board_read')
# @_jsonify
def board_read():
    # QQQ 작업 필요....
    # 제목, 글쓴이, 순서(등록/수정), 태그, 내용, 조건검색(날짜, startday-endday, 포스트 검색 보여줄 결과 수)
    # if query param is none, select limit 50
    ## 일단 paging...
    args  = request.args
    if len(args) == 0:
        posts =  Post.query.filter().order_by(desc(Post.registdt)).limit(10)
    
    response_data = [post._jsonify() for post in posts]
    result = { "result" : response_data, "b" : "DDD" , "ddd" : { "aaaa" : "ssss" }}
    result = json.dumps(result, ensure_ascii=False)
    
    response_data1 = [post.getJson() for post in posts]
    result1 = { "result" : response_data1, "b" : "DDD" , "ddd" : { "aaaa" : "ssss" }}
    result1 = json.dumps(result1, ensure_ascii=False)

    return result1  ## string으로 결과가 client에 가게 될 것임. json.loads()를 하면 서버에서는 dict로 처리함. client에 json으로 보내려면 jsonify()를 시켜줘야 함. 아니면 client에서 jsonify를 실행.. the JSON object must be str, bytes or bytearray, not dict
    # return result2

@bp.route('/')
def draw_board():
    result = board_read()
    result = json.loads(result, encoding='utf8')
    # result = string_to_dict(result)

    return render_template('board.html', result=result)


@bp.route('/post_read/<int:postno>')
def post_read(postno):
    post = Post.query.filter(Post.id == postno).first()
    if post is None:
        return { "result" : "not Found" }
    return post._jsonify()

@bp.route('/post', strict_slashes=False)
@bp.route('/post/<int:postno>')
@login_required
def post_write(method='GET', postno=None):
    print(">>>>>>>>>>>>>> user ", session['loginUser'])
    if postno is not None:
        post = post_read(postno)
        # if post.author != session['loginUser']:
        #     return x
        response_data = { "result" : post }
        return render_template('write.html', result=response_data)
    return render_template('write.html')

@bp.route('/post_create', methods=['POST'])
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

@bp.route('/post_update/<int:postno>', methods=['POST'])
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

@bp.route('/post_delete/<int:postno>', methods=['POST'])
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