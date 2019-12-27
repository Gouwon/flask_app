from sqlalchemy import Column, Integer, String, func, DateTime, func, BLOB
from .init_db import Base, db_session
import json
from collections import OrderedDict, namedtuple


class FlaskSession(Base):
    __tablename__ = 'flask_session'

    sid = Column(String(255), primary_key=True)
    value = Column(BLOB)

    @classmethod
    def chang(cls, sid, value):
        rec = db_session.query(cls).filter(cls.sid == sid).first()
        if not rec:
            rec = cls()
            rec.sid = sid
        rec.value = value

        return rec

class User(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    userid = Column(String(255))
    username = Column(String(255))
    password = Column(String(256))

    def __init__(self, username='guest', userid='0', password='', make_sha=False):
        self.username = username
        self.userid = userid
        self.password = func.sha2(password, 256) if make_sha else password
    
    def __repr__(self):
        return '<User %r %r>' % (self.username, self.password)

    def _jsonify(self):
        return json.dums({"username" : self.username, "userid" : self.userid})
    
class Post(Base):
    __tablename__ = 'Posts'
    id = Column(Integer, primary_key=True)
    head = Column(String(1024))
    content = Column(String(4048))
    author = Column(String(128))
    registdt = Column(DateTime, default=func.utc_timestamp())
    updatedt = Column(DateTime)

    def __init__(self, head, content, author):
        self.head = head
        self.content = content
        self.author = author
    
    def getupdatedt(self):
        return self.updatedt
    
    def setupdatedt(self):
        self.updatedt = func.utc_timestamp()
        return self.getupdatedt() 

    def __repr__(self):
        return '<Post %s by %s>' % (self.head, self.author)

    def _jsonify(self):
        return json.dumps({"head" : self.head, "content" : self.content, "author" : self.author}, ensure_ascii=False)
    
    def _getjson(self):
        return {"head" : self.head, "content" : self.content, "author" : self.author}

class QuertyConstructor(Post):
    def __init__(self, table=Post, **kwargs):
        self.table_model = table
        self.table = db_session.query(self.table_model)
        # self.data = self.__ordered_dict__(**kwargs)
        self.data = self.get_filterset(kwargs)
        self.sql_query = self.get_query(self.data)
        self.sql_inner_query = None
        
        w = get_filterset(data)
        # print("\n\n ",w)
        # table = 'Post'
        # self.table_query = 'Post.query'
        self.q = None
        self.inner_q = None

    @property
    def query(self):
        print("inside the getter")
        self.sql_query="second"
        return self.sql_query

    # w=list(filter(lambda e: e.x == 1, l))[0]
    def __ordered_dict__(self, unordered_dict):
        filts = namedtuple('filters', ['m', 'o', 'v'])
        result = []
        for k, v in unordered_dict.items():
            if k == 'pageno':
                k = 'offset'
            result.append(filters(m, k, v))

        return ordered_dict

    def get_filterset(self, dictionary):
        test = namedtuple("test", ["model", "attr", "value"])
        w = [ None for i in range(len(dictionary)-1)]
        insert_order = {"criteria" : "", "search" : 0, "order_by" : 1, "order" : 2, "limit" : 3, "offset" : 4}
        c = None
        for k, v in dictionary.items():
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



    # filterset = [test(model='sql.expression', operation='search', value=''), test(model='Post', operation='hasattr', value='head'), test(model='Post', operation='hasattr', value='registdt'), test(model='sql.expression', operation='order', value='desc'), test(model='sql.expression', operation='limit', value='10'), test(model='sql.expression', operation='offset', value='0')]

    def get_query(self, fl):
        '''filterset: (model, operation, value)
            :return query
        '''
        print(fl, type(fl))

        # [test(model='Post', attr='head', value='%글1%'), test(model='Post', attr='registdt', value='order_by'), test(model='sql.expression', attr='desc', value='order'), test(model='Post', attr='limit', value='10'), test(model='Post', attr='offset', value='0')]

        for l in fl:
            if l.model != 'sql.expression':
                self.inner_q = getattr(l.model, l.attr) if hasattr(l.model, l.attr) else None
                print("\n\n\n:::::::::::::::::::::", self.inner_q)
                if l.value != 'order_by':
                    self.inner_q = self.inner_q.like(l.value, escape='/')
                    self.q = self.table.filter(self.inner_q)
            else:
                if l.value == 'order':
                    qq = getattr(l.model, l.attr)(self.inner_q) if hasattr(l.model, l.attr) else None
                    self.q = self.q.order_by(qq)
                else:
                    qq = getattr(l.model, l.attr)(l.value) if hasattr(l.model, l.attr) else None
                    self.q = self.q.order_by(qq) 
