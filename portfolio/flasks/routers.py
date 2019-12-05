from flasks import app

@app.route('/')
def root():
    return 'this is root.'
