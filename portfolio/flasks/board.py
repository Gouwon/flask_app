from flask import Blueprint
from flask import render_template
from .models import Post

bp = Blueprint('bd', __name__, url_prefix='/board')

@bp.route('/')
def draw_board():
    return render_template('board.html')

@bp.route('/getbd')
def get_board():
