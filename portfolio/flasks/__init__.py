from flask import Flask

app = Flask(__name__)
app.debug = True

from . import routers
from . import auth
app.register_blueprint(auth.bp)

from . import init_db

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://dooo:root1!@localhost/dooodb?charset=utf8'

@app.before_first_request
def beforeFirstRequest():
    print('>>>>> before_first_request :: initialize db')
    init_db.init_db()

@app.teardown_appcontext
def teardownAppcontext(exception):
    print('>>>>> teardown_appcontext :: ', exception)
    init_db.db_session.remove() # remove used db_session

