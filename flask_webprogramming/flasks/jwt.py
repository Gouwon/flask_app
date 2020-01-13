from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, \
    get_jwt_identity, jwt_optional, get_jwt_claims, verify_jwt_in_request
from . import app
from .decorators import _jsonify
from functools import wraps

# Setup the Flask-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
jwt = JWTManager(app)


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
    ret = {'access_token': access_token}

    return jsonify(ret), 200


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
    print(">>>>> user_identity_lookup\n", user.username, "\n=================")
    return user.username

users_to_roles = {
    'foo': ['admin'],
    'bar': ['peasant'],
    'baz': ['peasant']
}

@jwt.user_loader_callback_loader
def user_loader_callback(identity):
    print("\n\n\n>>>> user_loader_callback()user_loader_callback() ", identity)
    if identity not in users_to_roles:
        return None

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
