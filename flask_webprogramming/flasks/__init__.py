import os
import errno
import logging
from uuid import uuid4
from collections import MutableMapping
from datetime import datetime, timedelta

import sqlite3
import pickle
from flask import Flask, session, render_template, url_for, request, \
                make_response
from flask.sessions import SessionInterface, SessionMixin
from werkzeug.datastructures import CallbackDict
from pymongo import MongoClient
from redis import Redis
from beaker.middleware import SessionMiddleware

from .decorators import _jsonify


app = Flask(__name__)
app.debug = True
app.debug_log_format = '%(levelname)s in %(model)s [%(lineno)d]: %(massage)s'

file_log_format = logging.Formatter('%(levelname)-8s %(message)s')
# file_logger = logging.FileHandler('flask_webprogramming.log')
file_logger = logging.FileHandler(
    'flask_webprogramming.log',
    mode='a',
    encoding='utf-8',
    delay=False
)
# log file under certain bytes
# rotating_file_logger = logging.handlers.RotatingFileHandler(
#     filename='flask_webprogramming.log',
#     mode='a',
#     maxBytes=10485760,  # 10MB = 1MB * 1024 * 1024 = 10485760
#     backupCount=5,  # once reached maxBytes, file will be splited untile 5.
#     encoding='utf-8',
#     delay=False
# )
file_logger.setFormatter(file_log_format)
# app.logger.addHandler(file_logger)

# setting log level display
# app.logger.setLevel(logging.INFO)
# handler.setLevel(logging.warning)

from . import routers
from . import restful
from . import jwt
# @app.route('/t', methods=['GET', 'POST'])
# def ttt():
#     if request.method == 'POST':
#         # print('\n\n\n\n==============')
#         # print(type(jwt.jwt))
#         # print('\n\n\n\n==============')
#         # print(jwt.jwt)
#         # print(str(jwt.jwt))

#         # print('\n\n\n==============')

#         # return jwt.jwt, 201, {'Content-Type': 'application/json'}
#         return {
#     "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGl0eSI6MSwiaWF0IjoxNDQ0OTE3NjQwLCJuYmYiOjE0NDQ5MTc2NDAsImV4cCI6MTQ0NDkxNzk0MH0.KPmI6WSjRjlpzecPvs3q_T3cJQvAgJvaQAPtk1abC_E"
# }, 201, {'Content-Type': 'application/json'}
#     return "TTT"

from . import auth
app.register_blueprint(auth.bp)

from . import board
app.register_blueprint(board.bp)

from .init_db import db_session, init_db
from .models import FlaskSession


@app.route('/log')
def logger():
    # SMTP log handler
    if app.debug:
        from logging.handlers import SMTPHandler

        ADMINS = ['']
        mail_handler = SMTPHandler(
            mailhost='localhost',
            fromaddr='seyosa5674@onmail.top',
            toaddrs=['jskd2938@gmail.com'],
            subject='Application Error'
        )
        # if smtp server requires user identity
        # mail_handler = SMTPHandler(
        #     mailhost=('smtp.gmail.com', 587), #if smtp port isn't 25.
        #     fromaddr='seyosa5674@onmail.top',
        #     toaddrs=['jskd2938@gmail.com'],
        #     subject='Mail Host',
        #     credentials=('jskd2938', 'password'),
        #     []  # gmail uses tls so adding an empty list as 6th argument.
        # )
        mail_handler.setFormatter(logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
        ))
        # app.logger.addHandler(mail_handler)

    app.logger.debug('>>>>> DEBUG 메세지를 출력합니다.')
    return '콘솔을 확인하여 주시기 바랍니다.'

# <-------------------------- session using beaker --------------------------->
session_opts = {
    'session.type': 'ext:memcached',
    'session.url': '127.0.0.1:11211',
    'session.data_dir': './cache',
}

class BeakerSessionInterface(SessionInterface):
    def open_session(self, app, request):
        session = request.environ['beaker.session']
        return session
    
    def save_session(self, app, session, response):
        session.save()

app.wsgi_app = SessionMiddleware(app.wsgi_app, session_opts)
app.session_interface = BeakerSessionInterface()
# <-------------------------- session using beaker --------------------------->

# <-------------------------- session using redis ---------------------------->
class RedisSession(CallbackDict, SessionMixin):
    def __init__(self, initial=None, sid=None, new=False):
        def on_update(self):
            self.modified = True
        CallbackDict.__init__(self, initial, on_update)
        self.sid = sid
        self.new = new
        self.modified = False

class RedisSessionInterface(SessionInterface):
    serializer = pickle
    session_class = RedisSession

    def __init__(self, redis=None, prefix='session:'):
        if redis is None:
            redis = Redis()
        self.redis = redis
        self.prefix = prefix

    def generate_sid(self):
        return str(uuid4())
    
    def get_redis_expiration_time(self, app, session):
        if session.permanent:
            return app.permanent_session_lifetime
        return timedelta(days=1)
    
    def open_session(self, app, request):
        sid = request.cookies.get(app.session_cookie_name)
        if not sid:
            sid = self.generate_sid()
            return self.session_class(sid=sid, new=True)
        val = self.redis.get(self.prefix + sid)
        if val is not None:
            data = self.serializer.loads(val)
            return self.session_class(data, sid=sid)
        return self.session_class(sid=sid, new=True)
    
    def save_session(self, app, session, response):
        domain = self.get_cookie_domain(app)
        if not session:
            self.redis.delete(self.prefix + session.sid)
            if session.modified:
                reponse.delete_cooke(app.session_cookie_name, domain=domain)
            return
        redis_exp = self.get_redis_expiration_time(app, session)
        val = self.serializer.dumps(dict(session))
        self.redis.setex(self.prefix + session.sid, \
                        val, int(redis_exp/total_seconds())
        )
        httponly = self.get_cookie_httponly(app)
        secure = self.get_cookie_secure(app)
        expires = self.get_expiration_time(app, session)

        reponse.set_cooke(app.session_cookie_name, session.sid, \
                        expires=expires, httponly=httponly, \
                        domain=domain, secure=secure)

app.session_interface = RedisSessionInterface()
app.config.update(
    SESSION_COOKIE_NAME='jpub_flask_session'
)
# <-------------------------- session using redis ---------------------------->

# <-------------------------- session using pymongo -------------------------->
class MongoSession(CallbackDict, SessionMixin):
    def __init__(self, initial=None, sid=None):
        CallbackDict.__init__(self, initial)
        self.sid = sid
        self.modified = False

class MongoSessionInterface(SessionInterface):
    def __init__(
                self, host='localhost', port=27017, \
                db='', collection='sessions'
    ):
        client = MongoClient(host, port)
        self.store = client[db][collection]

    def open_session(self, app, request):
        sid = request.cookies.get(app.session_cookie_name)
        if sid:
            stored_session = self.store.find_one({'sid': sid})
            if stored_session:
                if stored_session.get('expiration') > datetime.utcnow():
                    return MongoSession(initial=stored_sessi['data'],\
                                        sid=stored_session['sid'])
        sid = str(uuid4())
        return MongoSession(sid=sid)

    def save_session(self, app, session, response):
        domain = self.get_cookie_domain(app)
        if not session:
            response.delete_cookie(app.session_cookie_name, domain=domain)
            return
        if self.get_expiration_time(app, session):
            expiration = self.get_expiration_time(app, session)
        else:
            expiration = datetime.utcnow() + timedelta(hours=1)
        self.store.update(
            {'sid': session.sid},\
            {'sid': session.sid, 'data': session, 'expiration': expiration}, \
            True
        )
        response.set_cookie(app.session_cookie_name, session.sid, \
                            expires=self.get_expiration_time(app, session), \
                            httponly=True, domain=domain)

app.session_interface = MongoSessionInterface(db='jpub')
app.config.update(
    SESSION_COOKIE_NAME='jpub_flask_session'
)
# <-------------------------- session using pymongo -------------------------->


# <-------------------------- session using sqlite --------------------------->
class SqliteSession(SessionMixin, MutableMapping):
    _create_sql = \
        'CREATE TABLE IF NOT EXISTS session (key TEXT PRIMARY KEY, val BLOB)'
    _get_sql = 'SELECT val FROM session WHERE key = ?'
    _set_sql = 'REPLACE INTO session (key, val) values (?, ?)'
    _del_sql = 'DELETE FROM session WHERE key = ?'
    _ite_sql = 'SELECT key FROM session'
    _len_sql = 'SELECT COUNT(*) FROM session'

    def __init__(self, directory, sid, *args, **kwargs):
        sefl.path = os.path.join(directory, sid)
        self.directory = directory
        self.sid = sid
        self.modified = False
        self.conn = None
        if not os.path.exists(self.path):
            with self._get_conn() as conn:
                conn.execute(self._create_sql)
                self.new = True
        
    def __getitem__(self, key):
        key = pickle.dumps(key, 0)
        rv = None
        with  self._get_conn() as conn:
            for row in conn.execute(self._get_sql, (key,)):
                rv = pickle.loads(row[0])
                break
        if rv is None:
            raise KeyError('Key not in this session')
        return rv
    
    def __setitem__(self, key, value):
        key = pickle.dumps(key, 0)
        value = pickle.dumps(value, 2)
        with self._get_conn() as conn:
            conn.execute(self._set_sql, (key, value))
        self.modified = True
    
    def __delitem__(self, key):
        key = pickle.dumps(key, 0)
        with self._get_conn() as conn:
            conn.execute(self._del_sql, (key,))
        self.modified = True
    
    def __iter__(self):
        with self._get_conn() as conn:
            for row in conn.execute(self._ite_sql):
                yield pickle.loads(row[0])
    
    def __len__(self):
        with self._get_conn() as conn:
            for row in conn.execute(self._len_sql):
                return row[0]
    
    def _get_conn(self):
        if not self.conn:
            self.conn = sqlite3.Connection(self.path)
        return self.conn

    # These proxy classes are needed in order
    # for this session implementation to work properly.
    # That is because sometimes flask will chain method calls
    # with session 'setdefault' calls.
    # Eg: session.setdefault('_flashes', []).append(1)
    # method calls will be persisted back to the sqlite database

    class CallableAttributeProxy(object):
        def __init__(self, session, key, obj, attr):
            self.session = session
            self.key = key
            self.obj = obj
            self.attr = attr

        def __call__(self, *args, **kwargs):
            rv = self.attr(*args, **kwargs)
            self.session[self.key] = self.obj
            return rv
        
        class PersistedOvjectProxy(object):
            def __init__(self, session, key, obj):
                self.session = session
                self.key = key
                self.obj = obj

            def __getattr__(self, naem):
                attr = getattr(self.obj, name)
                if callable(attr):
                    return SqliteSession.CallableAttributeProxy(
                            self.session, self.key, self.obj, attr)
                return attr
            
            def setdefault(self, key, value):
                if key not in self:
                    self[key] = value
                    self.modified = True
                return SqliteSession.PersistedObjectProxy(self, key, self[key])

class SqliteSessionInterface(SessionInterface):
    def __init__(self, directory):
        directory = os.path.abspath(directory)
        if not os.path.exists(directory):
            os.mkdir(directory)
        self.directory = directory
    
    def open_session(self, app, session, request):
        sid = request.cookies.get(app.session_cookie_name)
        if not sid:
            sid = str(uuid4())
        rv = SqliteSession(self.directory, sid)
        return rv

    def save_session(self, app, session, response):
        domain = self.get_cookie_domain(app)
        if not session:
            try:
                os.unlink(session.path)
            except OSError as e:
                if e.errno != errno.ENOENT:
                    raise
                if session.modified:
                    response.delete_cookie(app.session_cooke_name, \
                                            domain=domain)
                return
            
            httponly = self.get_cookie_httponly(app)
            secure = self.get_cookie_secure(app)
            expires = self.get_expiration_time(app, session)

            response.set_cookie(app.session_cookie_name, seesion.sid,
                                expires=expires, httponly=httponly,
                                domain=domain, secure=secure)

path = '/tmp/app_session'
if not os.path.exists(path):
    os.mkdir(path)
    os.chmod(path, int('700', 8))

app.session_interface = SqliteSessionInterface(path)
app.config.update(
    SECRET_KEY='F1213lkfap',
    SESSION_COOKIE_NAME='jpub_flask_session'
)
# <-------------------------- session using sqlite --------------------------->

# <-------------------------- session using sqlalchemy ----------------------->
class Session(dict, SessionMixin):
    pass

class SQLAlchemySession(CallbackDict, SessionMixin):
    def __init__(self, initial=None, sid=None, new=False):
        def on_update(self):
            self.modified = True
        CallbackDict.__init__(self, initial, on_update)
        self.sid = sid
        self.new = new
        self.modified = False

class SQLAchemySessionInterface(SessionInterface):
    session_class = SQLAlchemySession
    serializer = pickle

    def generate_sid(self):
        return str(uuid4())

    def open_session(self, app, request):
        sid = request.cookies.get(app.session_cookie_name)
        if not sid:
            sid = self.generate_sid()
            return self.session_class(sid=sid, new=True)
        rec = db_session.query(FlaskSession) \
                        .filter(FlaskSession.sid == sid).first()
        
        if rec is not None:
            data = self.serializer.loads(rec.value)
            return self.session_class(data, sid=sid)
        return self.session_class(sid=sid, new=True)
    
    def save_session(self, app, session, response):
        domain = self.get_cookie_domain(app)
        if not session:
            rec = db_session.query(FlaskSession) \
                    .filter(FlaskSession.sid == session.sid).first()
            try:
                db_session.delete(rec)
                db_session.commit()
            except Exception as err:
                print(">>>>>>>>>>> save_session ", err)
                pass
            if session.modified:
                response.delete_cookie(app.session_cookie_name, domain=domain)
            
            return
            val = self.serializer.dumps(dict(session))
            session_db = FlaskSession.change(session.sid, val)
            db_session.add(session_db)
            db_session.commit()

            httponly = self.get_cookie_httponly(app)
            secure = self.get_cookie_secure(app)
            expires = self.get_expiration_time(app, session)

            response.set_cookie(app.session_cookie_name, session.sid,
                                expires=expires, httponly=httponly,
                                domain=domain, secure=secure)

app.session_interface = SQLAchemySessionInterface()
app.config.update(
    SECRET_KEY=os.urandom(60),
    SESSION_COOKIE_NAME='jpub_flask_session'
)
# <-------------------------- session using sqlalchemy ----------------------->

app.config.update(
    SECRET_KEY='',
    SESSION_COOKIE_NAME=''
)

app.config['SQLALCHEMY_DATABASE_URI'] \
    = 'mysql+pymysql://dooo:root1!@localhost/dooodb?charset=utf8'
# app.config['SECRET_KEY'] = 'development'

app.config.update(
    STRICT_SLASHED=False
)

@app.route('/session_in')
def session_signin():
    session['test'] = 'abc'
    return 'Session Signin'

@app.route('/session_out')
def session_signout():
    session.clear()
    return 'Session Signout'

@app.route('/session_stat')
def session_stat():
    print(session.get('test', 'Empty Data'))
    return 'Session Stat Print to Console'

@app.before_first_request
def beforeFirstRequest():
    print('>>>>> before_first_request :: initialize db')
    session['loginUser'] = "guest"
    init_db()

@app.teardown_appcontext
def teardownAppcontext(exception):
    print('>>>>> teardown_appcontext :: ', exception)
    db_session.remove() # remove used db_session

