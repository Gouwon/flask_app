from datetime import datetime
from functools import wraps

from flask import Flask, jsonify, request
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, \
    get_jwt_identity, jwt_optional, get_jwt_claims, verify_jwt_in_request,\
    jwt_refresh_token_required, create_refresh_token, get_current_user, fresh_jwt_required, token_in_blacklist_loader,
    get_raw_jwt, set_access_cookies, set_refresh_cookies, unset_jwt_cookies,
    get_csrf_token)

from . import app
from .decorators import _jsonify


# Setup the Flask-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
jwt = JWTManager(app)
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_ACCESS_COOKIE_PATH'] = '/api/'
app.config['JWT_REFRESH_COOKIE_PATH'] = '/token/refresh'


# Provide a method to create access tokens. The create_access_token()
# function is used to actually generate the token, and you can return
# it to the caller however you choose.
@app.route('/ttt', methods=['POST'])
def ttt():
    # if not request.is_json:
    #     return jsonify({"msg": "Missing JSON in request"}), 400

    # username = request.json.get('username', None)
    # password = request.json.get('password', None)
    # if not username:
    #     return jsonify({"msg": "Missing username parameter"}), 400
    # if not password:
    #     return jsonify({"msg": "Missing password parameter"}), 400

    # if username != 'test' or password != 'test':
    #     return jsonify({"msg": "Bad username or password"}), 401

    # Identity can be any data that is json serializable
    # access_token = create_access_token(identity=username)

        # Create an example UserObject
    # user = UserObject(username='test', roles=['foo', 'bar'])
    user = UserObject(username='foo', roles=['foo', 'bar'])


    # We can now pass this complex object directly to the
    # create_access_token method. This will allow us to access
    # the properties of this object in the user_claims_loader
    # function, and get the identity of this object from the
    # user_identity_loader function.
    access_token = create_access_token(identity=user)
    refresh_token = create_refresh_token(identity=user)

    ret = {'access_token': access_token,
        'refresh_token': refresh_token,
    }

    # With JWT_COOKIE_CSRF_PROTECT set to True, set_access_cookies() and
    # set_refresh_cookies() will now also set the non-httponly CSRF cookies
    # as wel
    res = jsonify({'login': True})
    set_access_cookies(res, access_token)
    set_refresh_cookies(res, refresh_token)

    # return jsonify(ret), 200
    return res
    


# Protect a view with jwt_required, which requires a valid access token
# in the request to access.
@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    # Access the identity of the current user with get_jwt_identity
    # get_jwt_identity will return identity of the JWT
    # current_user = get_jwt_identity()
    # return jsonify(logged_in_as=current_user), 200
    ret = {
        'current_identity': get_jwt_identity(),  # test
        'current_roles': get_jwt_claims()['roles']  # ['foo', 'bar']
    }


    ## return render_template(
    ##     "form.html", csrf_token=(get_raw_jwt() or {}).get("csrf")
    ## )
    return jsonify(ret), 200

# Partially protecting routes
@app.route('/partially-protected', methods=['GET'])
@jwt_optional
@_jsonify
def partially_protected():
    #if no JWT is sent in with the request, get_jwt_identity() will return None
    current_user = get_jwt_identity()
    if current_user:
        print("\n\n>>>>> current_user ", current_user, type(current_user))
        return {'logged_in_as': current_user}
    else:
        return {'logged_in_as': 'anonymous user'}

# Storing Data in Access Tokens      
# Using the user_claims_loader, we can specify a method that will be
# called when creating access tokens, and add these claims to the said
# token. This method is passed the identity of who the token is being
# created for, and must return data that is json serializable
# user_claims_loader decorator sets the callback function of create_access_token() function.
# last user_claims_loader decorator only be called.
# so this decorator and function won't be called cause another one defined below part.
@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    print(">>>>> add_claims_to_access_token\n\n\n=================")
    return {
        'hello': identity,
        'foo': ['bar', 'baz']
    }

# In a protected view, get the claims you added to the jwt with the
# get_jwt_claims() method
@app.route('/get_jwt_claims', methods=['GET'])
@jwt_required
def gjc():
    print(">>>>> before get_jwt_claims()")
    claims = get_jwt_claims()
    print(">>>>> after get_jwt_claims() ", claims)
    return jsonify({
        'hello_is': claims['hello'],
        'foo_is': claims['foo']
    }), 200

class UserObject():
    def __init__(self, username, roles):
        self.username = username
        self.roles = roles

# Create a function that will be called whenever create_access_token
# is used. It will take whatever object is passed into the
# create_access_token method, and lets us define what custom claims
# should be added to the access token.
@jwt.user_claims_loader
def add_role_to_access_token(user):
    print(">>>>> add_role_to_access_token\n", user,"\n=================")
    return {'roles': user.roles}
       
# Create a function that will be called whenever create_access_token
# is used. It will take whatever object is passed into the
# create_access_token method, and lets us define what the identity
# of the access token should be.
@jwt.user_identity_loader
def user_identity_lookup(user):
    print(">>>>> user_identity_lookup\n", user, "\n=================")
    return user.username

users_to_roles = {
    'foo': ['admin'],
    'bar': ['peasant'],
    'baz': ['peasant']
}

@jwt.user_loader_callback_loader
def user_loader_callback(identity):
    print("\n\n\n>>>> user_loader_callback()user_loader_callback() ", identity, type(identity))
    if identity not in users_to_roles:
        return None
    else:
        print('>>>> user_loader_callback()user_loader_callback() found!!!')

    return UserObject(
        username=identity,
        roles=users_to_roles[identity]
    )

@jwt.user_loader_error_loader
def custom_user_loader_error(identity):
    print("\n\n\n>>>> custom_user_loader_error()custom_user_loader_error() ", identity)
    ret = {
        "msg": "User {} not found".format(identity)
    }
    return jsonify(ret), 404

@app.route('/admin-only', methods=['GET'])
@jwt_required
def admin_only():
    print("\n\n\nadmin_only admin_only ")
    if 'admin' not in current_user.roles:
        return jsonify({"msg": "Forbidden"}), 403
    else:
        return jsonify({"msg": "don't forget to drink your ovaltine"})

def admin_required(fn):
    print("=======\nadmin_required decorator before wraps\n\n=========== fn", fn)
    @wraps(fn)
    def wrapper(*args, **kwargs):
        print("=======\wrapperwrapperwrapper inside a wrapper\n\n===========")
        verify_jwt_in_request()
        claims = get_jwt_claims()
        print("claimsclaimsclaims ", claims)
        if claims['roles'] != 'admin':
            return jsonify(msg='Admins only!'), 403
        else:
            return fn(*args, **kwargs)
    return wrapper

@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    print('\n\n\n>>>>> identity ', identity)
    print("=======\nadd_claims_to_access_token\n\n===========", identity.username, identity.roles)
    if identity.username == 'foo':
        return {'roles': 'admin'}
    else:
        return {'roles': 'peasant'}

@app.route('/admin_only', methods=['GET'])
@admin_required
def admin_only_approach():
    print("\n\n\nadmin_only_approachadmin_only_approach()")
    return jsonify(secret_message="go banana!") 

@app.route('/token/refresh', methods=['POST'])
@jwt_refresh_token_required
@_jsonify
def refresh():
    current_user = get_current_user()
    print("\n\n\n>>>>> current_user ", current_user, type(current_user))
    # ret = {
    #     'access_token': create_access_token(identity=current_user)
    # }
    # generate non-fresh access token
    ret = {
        'access_token': create_access_token(identity=current_user, fresh=False), 
    }

    # Set the access JWT and CSRF double submit protection cookies
    # in this response
    access_token = create_access_token(identity=current_user, fresh=False)

    # setting jwt access cookie in the response
    res = jsonify({'refresh': True})
    set_access_cookies(res, access_token)
    return ret

# making fresh token by logging in.
@app.route('/fresh_login', methods=['POST'])
@_jsonify
def fresh_login():
    # username = 'test'
    user = UserObject('bar', 'peasant')
    # password = 'test'
    if user.username != 'bar':
        return {'msg': 'Bad username or password'}, 401
    ret = {
        'access_token': create_access_token(identity=user, fresh=True)
    }
    return ret
    
# Only fresh JWTs can access this endpoint
@app.route('/protected_fresh', methods=['GET'])
@fresh_jwt_required
@_jsonify
def protected_fresh():
    username = get_jwt_identity()
    print('\n\n\n>>>>>> protected_freshprotected_fresh username ', username)
    return {'fresh_logged_in_as': username}

@app.route('/create_dev_token', methods=['POST'])
@jwt_required
@_jsonify
def create_dev_token():
    current_user = get_current_user()
    expires = datetime.timedelta(days=365)
    token = create_access_token(current_user, expires_delta=expires)
    return {'token': token}


# A storage engine to save revoked tokens. In production if
# speed is the primary concern, redis is a good bet. If data
# persistence is more important for you, postgres is another
# great option. In this example, we will be using an in memory
# store, just to show you how this might work. For more
# complete examples, check out these:
# https://github.com/vimalloc/flask-jwt-extended/blob/master/examples/redis_blacklist.py
# https://github.com/vimalloc/flask-jwt-extended/tree/master/examples/database_blacklist
blacklist = set()

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti  in blacklist

# Endpoint for revoking the current users access token
@app.route('/logout', methods=['DELETE'])
@jwt_required
def logout():
    jti = get_raw_jwt()['jti']
    blacklist.add(jti)
    return jsonify({"msg": "Successfully logged out"}), 200

# Endpoint for revoking the current users refresh token
@app.route('/logout2', methods=['DELETE'])
@jwt_refresh_token_required
def logout2():
    jti = get_raw_jwt()['jti']
    blacklist.add(jti)
    return jsonify({"msg": "Successfully logged out"}), 200

# Because the JWTs are stored in an httponly cookie now, we cannot
# log the user out by simply deleting the cookie in the frontend.
# We need the backend to send us a response to delete the cookies
# in order to logout. unset_jwt_cookies is a helper function to
# do just that.
@app.route('/token/remove', methods=['POST'])
def token_remove_from_cookie():
    res = jsonify({'logout': True})
    unset_jwt_cookies(res)
    return res

@app.route('/api/example', methods=['GET'])
@jwt_required
@_jsonify
def protected_api():
    current_user = get_current_user()
    username = get_jwt_identity()
    return {'hello': 'from {}'.format(username)}