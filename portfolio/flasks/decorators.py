from functools import wraps
from flask import session, request, url_for, make_response
import json

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session['loginUser'] is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def _jsonify(f):
    @wraps(f)
    def inner(*args, **kwds):
        r = f(*args, **kwds)
        result = make_response(json.dumps(r, ensure_ascii=False).encode("utf8"))
        return result
    return inner