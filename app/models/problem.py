from database import Base
from sqlalchemy import BigInteger, Boolean, Column, Integer, String

# export interface ProblemModel {
#   id: number;
#   user_address: string;
#   timestamp: number;
#   deadline: number;
#   title: string;
#   description: string;
#   reward: number;
#   solved: boolean;
#   submissions_count: number;
# }

class Problem(Base): 
    __tablename__ = 'problem'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_address = Column(String, nullable=True)
    timestamp = Column(BigInteger, nullable=True)
    deadline = Column(BigInteger, nullable=True)
    title = Column(String, nullable=True)
    description = Column(String, nullable=True)
    reward = Column(Integer, nullable=True)
    solved = Column(Boolean, nullable=False, default=False)
    submissions_count = Column(Integer, nullable=False, default=0)
    has_dataset = Column(Boolean, nullable=False, default=False)
    

    def __repr__(self):
        return "<Problem(id='%s', user_address='%s', timestamp='%s', deadline='%s', title='%s', description='%s', reward='%s', solved='%s', submissions_count='%s')>" % (self.id, self.user_address, self.timestamp, self.deadline, self.title, self.description, self.reward, self.solved, self.submissions_count)
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}