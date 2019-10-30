import os, sys
import tempfile

import pytest

module = os.path.join(os.path.split(os.path.dirname(os.path.abspath(__file__)))[0])
print(">>>>>>", module)
print(">>>>>>", sys.path)
if module not in sys.path:
    sys.path.append(module)
### before using this, should block this code so that python can find module in sys.path. after project usage end, delete custom module path from sys.path list.


from flaskr import create_app
from flaskr.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')

@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    ## tempfile.mkstemp() creates and opens a temporary file, returning the file object and the path to it. After the test is over, the temporary file is closed and removed.

    app = create_app({'TESTING':True, 'DATABASE':db_path,})
    ## TESTING tells Flask that the app is in test mode.

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

        yield app

        os.close(db_fd)
        os.unlink(db_path)

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

class  AuthActions(object):
    def __init__(self, client):
        self._client = client
    
    def login(self, username='test', password='test'):
        return self._client.post('/auth/login', data={'username':username, 'password':password})
        
    def logout(self):
        return self._client.get('/auth/logout')

@pytest.fixture
def auth(client):
    return AuthActions(client)