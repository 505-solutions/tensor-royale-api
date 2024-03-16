
from database import Base
from sqlalchemy import BigInteger, Boolean, Column, Float, Integer, String

# export interface DataModel {
#   id: number;
#   file_train: unknown; // nek zip file
#   description: string;
#   problem_id: number | null;
# }

class Data(Base):
    __tablename__ = 'data'
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(BigInteger, nullable=True)
    file_train = Column(String, nullable=True)
    description = Column(String, nullable=True)
    problem_id = Column(Integer, nullable=True)
    name = Column(String, nullable=True)
    size = Column(Float, nullable=True)

    def __repr__(self):
        data = self.as_dict()
        r = ""
        for k, v in data.items():
            r += f"{k}='{v}', "
        return f"<Data({r[:-2]})>"
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}