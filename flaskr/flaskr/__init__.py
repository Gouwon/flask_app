import os, sys
from flask import Flask



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    ## instance_relative_config attribute telling flask that the instance folder is located outside the flaskr package.
    app.config.from_mapping(
        SECRET_KEY=app.config,
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'))
    ## SECRET_KEY 'dev' will provide convenient value during development but when deploying it should be random value.
    ## app.instance_path make new directory named 'instance' and meaning this directory.


    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
        ## app.config.from_pyfile() get the configuration frome the config.py like real SECRET_KEY when deploying.
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.debug = True

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)
    ## The authentication blueprint will have views to register new users and to log in and log out.

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')
    ## app.add_url_rule() associates the endpoint name 'index' with the / url so that url_for('index') or url_for('blog.index') will both work, generating the same / URL either way

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    
    return app