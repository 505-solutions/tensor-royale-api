
from database import Base
from sqlalchemy import Boolean, Column, Integer, String

# export interface ModelTraining {
#   id: number;
#   problem_id: number | null;
#   data_id: number | null;
#   model: unknown; //nek natreniran model
# }


class Model(Base):
    __tablename__ = 'model'
    id = Column(Integer, primary_key=True, autoincrement=True)
    # problem_id = Column(Integer, nullable=True)
    description = Column(String, nullable=True)
    name = Column(String, nullable=True)
    author = Column(String, nullable=True)
    data_id = Column(Integer, nullable=True)
    model = Column(String, nullable=True)

    def __repr__(self):
        data = self.as_dict()
        r = ""
        for k, v in data.items():
            r += f"{k}='{v}', "
        return f"<Model({r[:-2]})>"
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}