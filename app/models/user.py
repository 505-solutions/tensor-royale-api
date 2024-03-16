from database import Base
from sqlalchemy import Column, Integer, String


class User(Base): 
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    wallet = Column(String, nullable=False)
  
    def __repr__(self): 
        return "<User(id='%s', wallet='%s', )>" % (self.id, self.wallet)
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}