from flask_server.init_db import Base, db_session
from sqlalchemy import Column, Integer, String, func, ForeignKey, DATE, MetaData, Table
from sqlalchemy.orm import relationship, joinedload, backref

class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True)
    email = Column(String)
    passwd = Column(String)
    nickname = Column(String)

    def __init__(self, email, passwd, nickname, make_sha=False):
        self.email = email
        self.nickname = nickname
        self.passwd = func.sha2(passwd, 256) if make_sha else passwd
        
    def get_json(self):
        return {"id" : self.id, "email" :  self.email, "password" : self.passwd, "nickname" : self.nickname}