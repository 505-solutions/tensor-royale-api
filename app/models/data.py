
from database import Base
from sqlalchemy import Boolean, Column, Integer, String

# export interface DataModel {
#   id: number;
#   file_train: unknown; // nek zip file
#   description: string;
#   problem_id: number | null;
# }

class Data(Base):
    __tablename__ = 'data'
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_train = Column(String, nullable=False)
    description = Column(String, nullable=False)
    problem_id = Column(Integer, nullable=True)

    def __repr__(self):
        return "<Data(id='%s', file_train='%s', description='%s', problem_id='%s')>" % (self.id, self.file_train, self.description, self.problem_id)
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}