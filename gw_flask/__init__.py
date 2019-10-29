from flask import Flask

app = Flask(__name__)
app.debug = True

@app.route('/')
def hello_world():
    return 'Hello, World!'

# Variable Rules
from flask import escape
@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % escape(username)
@app.route('/post/<int:post_id>')
def show_post(post_id):
    #show the post with the given id, the id is an integer
    return 'Post %d'% post_id
@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    #show the subpath after /path/
    return 'Subpath %s' % escape(subpath)

# Unique URLs / Redirection Behavior
@app.route('/projects/')
def projects():
    return 'The project page'
@app.route('/about')
def about():
    return 'The about page'

# URL Building
from flask import url_for
@app.route('/login')
def login():
    return 'login'

with app.test_request_context():
    print(url_for('hello_world'))
    print(url_for('login'))
    print(url_for('login', next='/about'))
    print(url_for('show_user_profile', username='John Doe'))

# HTTP Methods
from flask import request
@app.route('/slogin', methods=['GET', 'POST'])
def slogin():
    if request.method == 'POST':
        return "do_the_login()"
    else:
        return "show_the_login_form()"

# Static Files
#url_for('static', filename='style.css')

# Rendering Templates
from flask import render_template, session, g, get_flashed_messages
##from flask import Markup

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

# Accessing Request Data
# The Request Object
from flask import request

@app.route('/llogin', methods=['GET', 'POST'])
def llogin():
    if request.method == 'POST':
        if valid_login(request.form['username'], request.form['password']):
            return log_the_user_in(request.form['username'])
        else:
            error = 'Invalid username/password'
        # the code below is excuted if the request method
        # # was GET or the credentials were invalid
        return render_template('login.html', error=error)
@app.route('/search')
def search():
    searchword = request.args.get('key', '')

# File Uploads
## <input type="file" name="the_file" id="" enctype="multipart/form-data"> required
from werkzeug.utils import secure_filename

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['the_file']
        f.save('/var/' + secure_filename(f.filename))

# Cookies

@app.route('/h')
def index():
    username = request.cookies.get('username')
    # use cookies.get(key) instead of cookies[key] to not get a
    # KeyError if the cookie is missing.

from flask import make_response
###
@app.route('/h1')
def index1():
    resp = make_response(render_template('hello.html'))
    resp.set_cookie('username', 'the username')
    return resp

# Redirects and Errors
from flask import abort, redirect

@app.route('/h2')
def redirect():
    return redirect(url_for('login'))
@app.route('/login')
def abort():
    abort(401)
    this_is_never_executed()
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

# Sessions
# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def index():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return 'You are not logged in'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

# Hooking in WSGI Middleware

from werkzeug.middleware.proxy_fix import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app)
