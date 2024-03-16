from database import Base
from sqlalchemy import Column, Integer, String


class User(Base): 
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    wallet = Column(String, nullable=False)
    title = Column(String, nullable=False)
  
    def __repr__(self): 
        return "<User(id='%s', wallet='%s', title='%s')>" % (self.id, self.wallet, self.title)
    