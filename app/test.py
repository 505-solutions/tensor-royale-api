import random
import string

from database import SessionMaker
from models.data import Data
from models.model import Model
from models.problem import Problem
from models.result import Result
from models.submission import Submission
from models.user import User

# Print definitions
output = ""
output += "USER:\n"
output += str(User().as_dict()) + "\n"
output += "\n"
output += "PROBLEM:\n"
output += str(Problem().as_dict()) + "\n"
output += "\n"
output += "DATA:\n"
output += str(Data().as_dict()) + "\n"
output += "\n"
output += "MODEL:\n"
output += str(Model().as_dict()) + "\n"
output += "\n"
output += "SUBMISSION:\n"
output += str(Submission().as_dict()) + "\n"
output += "\n"
output += "RESULT:\n"
output += str(Result().as_dict()) + "\n"
output += "\n"
print(output)

with open("output.tmp", "w") as text_file:
    text_file.write(output)

# Structure
# USER:
# {'id': None, 'wallet': None}

# PROBLEM:
# {'id': None, 'user_address': None, 'timestamp': None, 'deadline': None, 'title': None, 'description': None, 'reward': None, 'solved': None, 'submissions_count': None}

# DATA:
# {'id': None, 'file_train': None, 'description': None, 'problem_id': None, 'test': None}

# MODEL:
# {'id': None, 'problem_id': None, 'data_id': None, 'model': None}

# SUBMISSION:
# {'id': None, 'user_id': None, 'model_id': None}

# RESULT:
# {'id': None, 'model_id': None, 'data_id': None, 'submission_id': None, 'result': None}

# Test data population
session = SessionMaker()

def random_string():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))

def user():
    u = User(wallet=random_string())
    session.add(u)
    session.commit()
    session.refresh(u)
    return u

users = [user() for _ in range(random.randint(1, 10))]

def problem(user):
    p = Problem(user_address=user.wallet, title=random_string(), description=random_string(), reward=random.randint(1, 100))
    session.add(p)
    session.commit()
    session.refresh(p)
    return p

problems = [problem(random.choice(users)) for _ in range(random.randint(1, 10))]



user = User(wallet="0x123")
session.add(user)
session.commit()
session.refresh(user)

problem = Problem(user_address=user.wallet, title="Problem 1", description="Description 1", reward=100)
session.add(problem)
session.commit()
session.refresh(problem)

data = Data(file_train="file.zip", description="Description 1", problem_id=problem.id)
session.add(data)
session.commit()
session.refresh(data)

model = Model(problem_id=problem.id, data_id=data.id, model="model.zip")
session.add(model)
session.commit()
session.refresh(model)

submission = Submission(user_id=user.id, model_id=model.id)
session.add(submission)
session.commit()
session.refresh(submission)

result = Result(model_id=model.id, data_id=data.id, submission_id=submission.id, result="result.zip")
session.add(result)
session.commit()
session.refresh(result)

session.close()
print("Tested")