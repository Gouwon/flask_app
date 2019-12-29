from flasks import app
from flask import render_template, request

@app.route('/')
def root():
    return render_template('base.html')

@app.route('/test', methods=['GET', 'POST'])
@app.route('/test/<int:post_no>')
def test(post_no=0):
    print(request.args.get('method'))
    return render_template('test.html')