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
    
# def like():
#     def nested_function(obj, func_name):
#         return " %s 입니다. " % func_name
#     return nested_function(obj, func_name)

def params_to_query(**kwargs):
    # {'order': 'desc', 'criteria': 'head', 'search': '', 'limit': '20'}
    post_columns= { "head" : like(), "content" : like(), "author" : "" }
    table = Post
    params = kwargs
    print("||||||||||||| ", kwargs)
    
    params['criteria']


    Post.query.filter(Post.head.like("%글1%", escape='/')).order_by(sql.expression.desc(Post.registdt)).limit(10).offset(10)
    



def query_db(table, **kwargs):
    q = db_session.query(table)
    print(">>>>>>>>>>> ", kwargs)
    for k, v in kwargs.items():
        f = getattr(table, k)
        print("<<<<<<<<" , f)
        q = q.filter(f.like(v, escape="/")) 
        print("\n\n\n, q", q)
    return q.all()


def get_filterset(dictionary):
    w = [ None for i in range(len(dictionary)-1)]
    insert_order = {"criteria" : "", "search" : 0, "order_by" : 1, "order" : 2, "limit" : 3, "offset" : 4}
    c = None
    for k, v in data.items():
        m = 'Post'
        if k == 'pageno':
            k = 'offset'
        i = insert_order[k]

        if k == 'search':
            k = c
            

        if k == 'criteria':
            c = v
            continue

        if k == 'order_by':
            k, v = v , "order_by"

        if k == 'order':
            m = 'sql.expression'
            k, v = v, k

        w[i] = test(m, k, v)
    return w



table = 'Post'
table_query = 'Post.query'
q = None
inner_q = None

# filterset = [test(model='sql.expression', operation='search', value=''), test(model='Post', operation='hasattr', value='head'), test(model='Post', operation='hasattr', value='registdt'), test(model='sql.expression', operation='order', value='desc'), test(model='sql.expression', operation='limit', value='10'), test(model='sql.expression', operation='offset', value='0')]

def get_query(fl):
    '''filterset: (model, operation, value)
        :return query
    '''
    print(fl, type(fl))

    # [test(model='Post', attr='head', value='%글1%'), test(model='Post', attr='registdt', value='order_by'), test(model='sql.expression', attr='desc', value='order'), test(model='Post', attr='limit', value='10'), test(model='Post', attr='offset', value='0')]

    for l in fl:
        if fl.model != 'sql.expression':
            inner_q = getattr(fl.model, fl.attr) if hasattr(fl.model, fl.attr) else None
            if fl.value != 'order_by':
                inner_q = inner_q.like(fl.value, escape='/')
                q = table_query.filter(inner_q)
        else:
            if fl.value == 'order':
                qq = getattr(fl.model, fl.attr)(inner_q) if hasattr(fl.model, fl.attr) else None
                q = q.order_by(qq)
            else:
                qq = getattr(fl.model, fl.attr)(fl.value) if hasattr(fl.model, fl.attr) else None
                q = q.order_by(qq)