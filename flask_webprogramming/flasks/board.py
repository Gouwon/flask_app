from flask import Blueprint, render_template, make_response, jsonify, \
                request, session, redirect, url_for, Response, request
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
        print('\n>>>>> data ', data)

        _offset = int(data['offset']) * int(data['limit']) \

        post_sql = Post.query.filter( \
            getattr(Post, data['criteria']).like(data['search'])). \
            order_by( \
                getattr(sql, data['order'])(getattr(Post, data['order_by'])))
                   
        counts = round(post_sql.count() / int(data['limit']))
        s = post_sql.limit(10).offset(1200).count()
        print("\n>>>>> s ", s)
        posts = post_sql.limit(data['limit']).offset(_offset)
    else:
        post_sql = Post.query.filter().order_by(sql.desc(Post.registdt))
        _offset = 0
        counts = round(post_sql.count() / 20)
        posts = post_sql.limit(20).offset(0)
    
    posts = [post._getjson() for post in posts]

    return json.dumps({'result': posts, 'page': (counts, _offset)}, \
                    ensure_ascii=False)

@bp.route('/', strict_slashes=False)
# @cached(timeout=10 * 60, key='board/%s')
def draw_board():
    result = get_posts()
    result = json.loads(result, encoding='utf8')

    return render_template('board.html', result=result)

# C R U D

# create post
@bp.route('/post/c/', methods=['GET', 'POST'])
@_jsonify
def create_post():
    data = request.get_json()
    head = data['head']
    content = data['content']
    author = session['loginUser']['id']
    post = Post(head=head, content=content, author=author)
    try:
        db_session.add(post)
        db_session.commit()
        msg = 'success'
    except Exception as err:
        print(">>>>> create_post err ", err)
        db_session.rollback()
        msg = 'failed'
    return {'result': msg}

# read post
@bp.route('/post/r/<int:postno>', methods=['GET'])
def read_post(postno, obj=False):
    post = Post.query.filter(Post.id == postno).first()
    if obj:
        return post
    post = post._getjson() if post is not None else {'result': None}
    return json.dumps(post, ensure_ascii=False)

# update post
@bp.route('/post/u/<int:postno>', methods=['POST'])
@_jsonify
def update_post(postno):
    post = read_post(postno, obj=True)
    data = request.form
    post.head = data['head']
    post.content = data['content']
    try:
        db_session.add(post)
        db_session.commit()
        msg = 'sucess'
    except Exception as err:
        print(">>>>> update_post err ", err)
        db_session.rollback()
        msg = 'failed'
    return {'result': msg}

# delete post
@bp.route('/post/d/<int:postno>', methods=['POST'])
@_jsonify
def delete_post(postno):
    post = read_post(postno=postno, obj=True)
    try:
        db_session.delete(post)
        db_session.commit()
        msg = 'sucess'
    except Exception as err:
        print(">>>>> delete_post err ", err)
        db_session.rollback()
        msg = 'failed'
    return {'result': msg}

# draw post.html
@bp.route('/post/<int:postno>', methods=['GET'])
def draw_post(postno):
    post = read_post(postno)
    post = json.loads(post, encoding='utf8')
    return render_template('post.html', result=post)

# draw write.html
@bp.route('/post/w', strict_slashes=False, methods=['GET'])
@bp.route('/post/w/<int:postno>', methods=['GET'])
def draw_write(postno=None):
    if postno is not None:
        post = read_post(postno=postno)
        post = json.loads(post, encoding='utf8')
        return render_template('write.html', result=post)
    return render_template('write.html', result={'resutl': None})
    