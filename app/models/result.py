
from database import Base
from sqlalchemy import Boolean, Column, Integer, String


class Result(Base):
    __tablename__ = 'result'
    id = Column(Integer, primary_key=True, autoincrement=True)
    model_id = Column(Integer, nullable=True)
    data_id = Column(Integer, nullable=True)
    submission_id = Column(Integer, nullable=True)
    result = Column(String, nullable=True)

    def __repr__(self):
        return "<Result(id='%s', model_id='%s', data_id='%s', result='%s')>" % (self.id, self.model_id, self.data_id, self.result)
    
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}