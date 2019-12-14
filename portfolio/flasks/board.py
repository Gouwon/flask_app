from flask import Blueprint
from flask import render_template, make_response, jsonify, request
from jinja2 import Markup
from .utils import _jsonify
from .models import Post
from .init_db import db_session

from pprint import pprint


bp = Blueprint('bd', __name__, url_prefix='/board')

@bp.route('/')
def draw_board():
    return render_template('board.html')

@bp.route('/getbd')
@_jsonify
def get_board():
    posts = Post.query.all()
    posts = [post._jsonify() for post in posts]
    print(posts)
    res = { 'data' : posts }
    return res

@bp.route('/<int:post_no>', methods=['GET', 'POST', 'DELETE'])
@_jsonify
def get_post(post_no):
    print(">>>>>>>>> request.method ", request.method)
    post = Post.query.filter(Post.id==post_no).first()

    if request.method == 'POST':
        data = request.get_json()
        post.head, post.content = data["head"], data["content"]
        
        try:
            db_session.commit()
            msg = "UPDATE COMPLETED"
        except Exception as sqlerr:
            print("\n>>>>>>>>>> sqlerr ", sqlerr)
            db_session.rollback()
            msg = "UPDATE FAILED"
        return {"result" : msg}
    elif request.method == 'DELETE':
        try:
            db_session.delete(post)
            msg = "DELETE COMPLETED"
        except Exception as sqlerr:
            print("\n>>>>>>>>>> sqlerr ", sqlerr)
            db_session.rollback()
            msg = "DELETE FAILED"
        
        return {"result" : msg}
    
    return post._jsonify() if (post is not None) else {"result" : msg}

