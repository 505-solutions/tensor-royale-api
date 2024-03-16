
from database import Base
from sqlalchemy import Boolean, Column, Integer, String


class Submission(Base):
    __tablename__ = 'submission'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=True)
    model_id = Column(Integer, nullable=True)

    def __repr__(self):
        return "<Submission(id='%s', user_id='%s', model_id='%s')>" % (self.id, self.user_id, self.model_id)
