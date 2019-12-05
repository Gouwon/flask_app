from sqlalchemy import Column, Integer, String, func
from .init_db import Base, db_session

class User(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    userid = Column(String(255))
    username = Column(String(255))
    password = Column(String(256))

    def __init__(self, username='guest', userid='0', password='', maeke_sha=False):
        self.username = username
        self.userid = userid
        self.password = func.sha2(password, 256) if make_sha else password
    
    def __repr__(self):
        return '<User %r %r>' % (self.username, self.password)