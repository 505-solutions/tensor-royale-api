import random
import string

from database import SessionMaker
from models.data import Data
from models.model import Model
from models.problem import Problem
from models.result import Result
from models.submission import Submission
from models.user import User

N_USERS = 3
N_PROBLEMS = 5
N_DATAS = 10
N_MODELS = 10
N_SUBMISSIONS = 15
N_RESULTS = 20

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
# {'id': None, 'name': None, 'file_train': None, 'description': None, 'problem_id': None, 'test': None}

# MODEL:
# {'id': None, 'problem_id': None, 'data_id': None, 'model': None}

# SUBMISSION:
# {'id': None, 'user_id': None, 'model_id': None, 'results': None}

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

users = [user() for _ in range(N_USERS)]

def problem(user):
    p = Problem(
        user_address=user.wallet, 
        title=random_string(), 
        description=random_string(), 
        reward=random.randint(1, 100),
        deadline=random.randint(10000000, 110101110100),
        timestamp=random.randint(194102302, 1100021000)
    )
    session.add(p)
    session.commit()
    session.refresh(p)
    return p

problems = [problem(random.choice(users)) for _ in range(N_PROBLEMS)]

def data(problem):
    d = Data(file_train=random_string(), description=random_string(), problem_id=problem.id)
    session.add(d)
    session.commit()
    session.refresh(d)
    return d

datas = [data(random.choice(problems)) for _ in range(N_DATAS)]

def model(problem, data):
    m = Model(data_id=data.id, model=random_string(), description=random_string(), name=random_string())
    session.add(m)
    session.commit()
    session.refresh(m)
    return m

models = [model(random.choice(problems), random.choice(datas)) for _ in range(N_MODELS)]

def submission(user, model):
    s = Submission(user_id=user.id, model_id=model.id)
    session.add(s)
    session.commit()
    session.refresh(s)
    return s

submissions = [submission(random.choice(users), random.choice(models)) for _ in range(N_SUBMISSIONS)]

def result(model, data, submission):
    r = Result(model_id=model.id, data_id=data.id, submission_id=submission.id, result=random_string())
    session.add(r)
    session.commit()
    session.refresh(r)
    return r

results = [result(random.choice(models), random.choice(datas), random.choice(submissions)) for _ in range(N_RESULTS)]
session.close()

print("Tested")