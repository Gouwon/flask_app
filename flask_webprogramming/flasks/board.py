from flask import Blueprint, render_template, make_response, jsonify, \
                request, session, redirect, url_for, Response
from jinja2 import Markup
from sqlalchemy import sql
import sqlalchemy
from .models import Post, QuertyConstructor
from .init_db import db_session
import json
from .decorators import login_required, _jsonify
from .utils import string_to_dict, params_to_query, query_db

from pprint import pprint


bp = Blueprint('bd', __name__, url_prefix='/board')




# returning params to dictionary
def p_to_j(**kwargs):
    return kwargs

# board post pagination
@bp.route('/board_read')
def get_posts():
    if request.args:
        data = p_to_j(**request.args)
        _offset = (int(data['offset']) - 1) * int(data['limit']) \
                if int(data['offset']) > 0 else 0 

        posts = Post.query.filter( \
            getattr(Post, data['criteria']).like(data['search'])). \
            order_by( \
                getattr(sql, data['order'])(getattr(Post, data['order_by']))).\
                limit(data['limit']).offset(_offset)
    else:
        posts = Post.query.filter(). \
                order_by(sql.desc(Post.registdt)).limit(20).offset(0)
    
    posts = [post._getjson() for post in posts]

    return json.dumps({'result': posts}, ensure_ascii=False)

@bp.route('/')
# @cached(timeout=10 * 60, key='board/%s')
def draw_board():
    result = get_posts()
    result = json.loads(result, encoding='utf8')

    return render_template('board.html', result=result)


@bp.route('/post_read/<int:postno>')
def post_read(postno):
    post = Post.query.filter(Post.id == postno).first()
    if post is None:
        return {"result": "not Found"}
    return post._getjson()

@bp.route('/post/<int:postno>', methods=['GET'])
def draw_post(postno):
    post = post_read(postno)
    return render_template('post.html', result=post)

@bp.route('/post', strict_slashes=False)
@bp.route('/post/<int:postno>', methods=['POST'])
@login_required
def post_write(method='GET', postno=None):
    # print(">>>>>>>>>>>>>> user ", session['loginUser'])
    if postno is not None:
        post = post_read(postno)
        response_data = { "result" : post }
        return render_template('write.html', result=response_data)
    return render_template('write.html')

@bp.route('/post_create', methods=['POST'])
@_jsonify
def post_create():
    # data = request.args.to_dict(flat=False) param
    received_data = request.get_json()
    input_data = received_data['data']

    post = Post(head=input_data['head'], content=input_data['content'], \
                author=session['loginUser']['id'])

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
def post_update(postno):
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
def post_delete(postno):
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