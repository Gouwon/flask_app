from sqlalchemy import Column, Integer, String, func, DateTime, func
from .init_db import Base, db_session
import json


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
    
    def getJson(self):
        return {"head" : self.head, "content" : self.content, "author" : self.author}