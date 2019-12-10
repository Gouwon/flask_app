from sqlalchemy import Column, Integer, String, func, DateTime
from .init_db import Base, db_session

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
        return {"username" : self.username, "userid" : self.userid}
    
class Post(Base):
    __tablename__ = 'Posts'
    id = Column(Integer, primary_key=True)
    head = Column(String(1024))
    content = Column(String(4048))
    author = Column(String(128))
    registdt = Column(DateTime)

    def __init__(self, head, content, author):
        self.head = head
        self.content = content
        self.author = author

    def __repr__(self):
        return '<Post %s by %s>' % (self.head, self.author)

    def _jsonify(self):
        return {"head" : self.head, "content" : self.content, "author" : self.author}