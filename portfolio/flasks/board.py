from flask import Blueprint
from flask import render_template, make_response, jsonify, request
from jinja2 import Markup
from .utils import _jsonify
from .models import Post

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

@bp.route('/<int:post_no>', methods=['GET', 'POST'])
@_jsonify
def get_post(post_no):
    print(">>>>>>>> method", request.method)
    if request.method == 'POST':
        # QQQQ 삭제 처리 작업 필요
        # pprint(request.form)
        print(">>>>>>>>>>> request.get_json()", request.get_json(), type(request.get_json()))
        pprint(request.headers)
        print("================")
        print(">>>>>>>>>> request.is_json()", request)
        # data = request.get_json()
        print(">>>>>> type of request.headers", type(request.headers))

        return "OK"
    
    post = Post.query.filter(Post.id==post_no).first()

    return post._jsonify() if (post is not None) else "찾으시는 게시글이 없습니다."

