from flasks import app
from flask import render_template, request

@app.route('/')
def root():
    return 'this is root.'

@app.route('/test', methods=['GET', 'POST'])
@app.route('/test/<int:post_no>')
def test(post_no=0):
    print(method)
    print(request.args.get('method'))
    return render_template('post.html')