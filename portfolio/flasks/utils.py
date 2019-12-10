from functools import wraps
from flask import make_response
import json

def _jsonify(f):
    @wraps(f)
    def inner(*args, **kwds):
        r = f(*args, **kwds)
        result = make_response(json.dumps(r, ensure_ascii=False))
        return result
    return inner