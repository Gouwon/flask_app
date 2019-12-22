import json, re
from .init_db import db_session
from sqlalchemy import sql
from .models import Post

def string_to_dict(*args, **kwargs):
    data = args[0]
    values = [str(type(x)) for x in data.values()]
    _isdict = True if str(type(data)) == "<class 'dict'>" else False
    _haslist = True if "<class 'list'>" in values else False

    if _isdict is True and _haslist is True:
        for k in data:
            _islist = True if str(type(data[k])) == "<class 'list'>" else False
            pattern = re.compile('{')
            target = [ pattern.match(y) for y in args[0][k] ]
            _hasdict = True if target.count(None) == 0 else False
            if _islist is True and _hasdict is True:
                data[k] = list(map(lambda x : json.loads(x, encoding='utf8'), data[k]))
            else:
                pass

    return data
    
def like():
    def nested_function(obj, func_name):
        return " %s 입니다. " % func_name
    return nested_function(obj, func_name)

def params_to_query(**kwargs):
    # {'order': 'desc', 'criteria': 'head', 'search': '', 'limit': '20'}
    post_columns= { "head" : like(), "content" : like(), "author" : "" }
    table = Post
    params = kwargs
    print("||||||||||||| ", kwargs)
    
    params['criteria']


    # Post.query.filter(Post.head.like("%글1%", escape='/')).order_by(sql.expression.desc(Post.registdt)).limit(10).offset(10)
    



def query_db(table, **kwargs):
    q = db_session.query(table)
    for k, v in kwargs.items():
        f = getattr(table, k)
        q = q.filter(f.like(v, escape="/")) 
    return q.all()


