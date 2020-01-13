import json
from functools import wraps

from flask import session, request, url_for, make_response, \
                redirect, render_template, flash
from werkzeug.contrib.cache import RedisCache
from flask_jwt_extended import JWTManager, verify_jwt_in_request, create_access_token, get_jwt_claims
from _datetime import datetime


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('loginUser', 'guest') == 'guest':
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


cache = RedisCache()
def cached(timeout=5 * 60, key='view/%s'):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            cache_key = key % request.path
            rv = cache.get(cache_key)
            if rv is not None:
                return rv
            rv = f(*args, **kwargs)
            cache.set(cache_key, rv, timeout=timeout)
            return rv
        return decorated_function
    return decorator

def templated(template=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            template_name = template
            if template_name is None:
                template_name = request.endpoit.replace('.','/') + '.html'
            ctx = f(*args, **kwargs)
            if ctx is None:
                ctx = {}
            elif not isinstance(ctx, dict):
                return ctx
            return render_template(template_name, **ctx)
        return decorated_function
    return decorator

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # redirect to login if guest
        if session.get('loginUser', 'guest') is 'guest':
            return redirect(url_for('auth.login', next=request.url))
        # check user authority
        # QQQ 유저별 권한을 로그인시, 어떻게 확인하여, 세션 혹은 기타 등등에 저장할것인가?
        if 'R' not in session['access_auth']:
            return redirect(url_for('/'))
        return f(*args, **kwargs)
    return decorated_function

def role(role):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if role not in session.get('access_auth', 'S'):
                flash(u'허가되지 않은 사용자입니다.')
                return redirect(request.referrer)
            return f(*args, **kwargs)
        return decorated_function
    return wrapper

def no_cache(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        res = make_response(f(*args, **kwargs))
        h = res.headers
        h['Last-Modified'] = datetime.datetime.now()
        h['Cache-Control'] = 'no-store, no-cache, must-revalidate, \
                            post-check=0, pre-check=0'
        h['Pragma'] = 'no-cache'

        return res
    return decorated_function

def _jsonify(f):
    @wraps(f)
    def inner(*args, **kwds):
        r = f(*args, **kwds)
        result = make_response(json.dumps(r, ensure_ascii=False).encode("utf8"))
        return result
    return inner

