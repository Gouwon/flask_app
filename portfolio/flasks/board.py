from flask import Blueprint
from flask import render_template, make_response, jsonify
from jinja2 import Markup
from .utils import _jsonify
from .models import Post

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
