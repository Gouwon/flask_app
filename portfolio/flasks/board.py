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
    return render_template('board.html')

# reading board
@bp.route('/board_read')
@_jsonify
def board_read():
    # if query param is none, select limit 50
    args  = request.args
    if args is None:
        posts =  Post.query.filter().order_by(desc(Post.registdt)).limit(50)
    
    print("?????? ", args)
    print("args.items()args.items()args.items()args.items() ", args.items())
    print(",,,,,,,,,,,,,,,,,,,,,", args.to_dict(False))
    v = args.to_dict(flat=False)
    print("%(s)s %(v)s %(c)s" % v)

    for a in args.items():
        print("/////// ", a)


    for c in args.keys():
        print(c)
    # posts = [post._jsonify() for post in posts]

    # return posts
    return "OK"