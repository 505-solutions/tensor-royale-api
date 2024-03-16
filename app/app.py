
import requests
from database import SessionMaker, database_uri, init_db
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from models.data import Data
from models.model import Model
from models.problem import Problem
from models.result import Result
from models.submission import Submission
from models.user import User

app = Flask(__name__)
# setup cors that allows * to be origin
CORS(app)
app.config.update(
    SQLALCHEMY_DATABASE_URI=database_uri,
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)
print(database_uri)

# initialize the database connection
db = SQLAlchemy(app)

# start app migration
migrate = Migrate(app, db)

# create all needed db objects
init_db()

# run app
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)

# run tests to make sure db works
import test

from helper import debug_json

VALIDATOR_URL = "https://tensorroyale-prover.alpi314.com/"

# Routes
@app.route('/')
def index():
    return 'Hello, World!'

# User routes
@app.route('/users', methods=['POST'])
def users():
    session = SessionMaker()
    users = session.query(User).all()
    session.close()

    return jsonify([user.as_dict() for user in users])

# Problem routes
@app.route('/problems', methods=['POST'])
def problems():
    session = SessionMaker()
    user_address = request.get_json().get('user_address', None)
    if user_address:
        problems = session.query(Problem).filter_by(user_address=user_address).all()
    else:
        problems = session.query(Problem).all()
    session.close()

    return jsonify([problem.as_dict() for problem in problems])

@app.route('/problems/get', methods=['POST'])
def get_problem():
    session = SessionMaker()
    problem_id = request.get_json()['id']
    problem = session.query(Problem).filter_by(id=problem_id).first()
    session.close()

    return jsonify(problem.as_dict())

@app.route('/problems/create', methods=['POST'])
def create_problem():
    session = SessionMaker()
    data = request.get_json()
    problem = Problem(**data)
    session.add(problem)
    session.commit()

    session.refresh(problem)
    session.close()

    response = requests.post(VALIDATOR_URL + "problem", json=debug_json(problem.as_dict()), headers={"Content-Type": "application/json"})
    data = problem.as_dict()
    data["hash"] = response.text
    return jsonify(data)

@app.route('/problems/update', methods=['POST'])
def update_problem():
    session = SessionMaker()
    data = request.get_json()
    problem = session.query(Problem).filter_by(id=data['id']).first()
    for key in data:
        setattr(problem, key, data[key])
    session.commit()
    session.close()

    return jsonify(problem.as_dict())

@app.route('/problems/delete', methods=['POST'])
def delete_problem():
    session = SessionMaker()
    problem_id = request.get_json()['id']
    problem = session.query(Problem).filter_by(id=problem_id).first()
    session.delete(problem)
    session.commit()
    session.close()

    return jsonify(problem.as_dict())

# Data routes
@app.route('/data', methods=['POST'])
def data():
    problem_id = request.get_json().get('problem_id', None)
    author = request.get_json().get('author', None)
    filter = {
        'problem_id': problem_id,
        'author': author
    }
    session = SessionMaker()
    data = session.query(Data).filter_by(**{k: v for k, v in filter.items() if v is not None}).all()
    session.close()

    outputs = []
    for datum in data:
        outputs.append(datum.as_dict())

    for output in outputs:
        results = session.query(Problem).filter_by(id=output['problem_id'])
        if results.count() > 0:
            output['problem'] = results.first().as_dict()
        else:
            output['problem'] = None

    return jsonify(outputs)

@app.route('/data/get', methods=['POST'])
def get_data():
    session = SessionMaker()
    data_id = request.get_json()['id']
    datum = session.query(Data).filter_by(id=data_id).first()
    session.close()

    return jsonify(datum.as_dict())

@app.route('/data/create', methods=['POST'])
def create_data():
    session = SessionMaker()
    data = request.get_json()
    datum = Data(**data)
    session.add(datum)
    # session.refresh(datum)
    

    problem = session.query(Problem).filter_by(id=datum.problem_id).first()
    if problem:
        problem.has_dataset = True
    session.commit()
    session.refresh(datum)
    session.close()

    response = requests.post(VALIDATOR_URL + "dataset", json=debug_json(datum.as_dict()), headers={"Content-Type": "application/json"})
    data = datum.as_dict()
    data["hash"] = response.text
    return jsonify(data)

@app.route('/data/update', methods=['POST'])
def update_data():
    session = SessionMaker()
    data = request.get_json()
    datum = session.query(Data).filter_by(id=data['id']).first()
    for key in data:
        setattr(datum, key, data[key])
    session.commit()
    session.close()

    return jsonify(datum.as_dict())

@app.route('/data/delete', methods=['POST'])
def delete_data():
    session = SessionMaker()
    data_id = request.get_json()['id']
    datum = session.query(Data).filter_by(id=data_id).first()
    session.delete(datum)
    session.commit()
    session.close()

    return jsonify(datum.as_dict())

# Model routes
@app.route('/models', methods=['POST'])
def models():
    session = SessionMaker()
    author = request.get_json().get('author', None)
    if author:
        models = session.query(Model).filter_by(author=author).all()
    else:
        models = session.query(Model).all()
    session.close()

    return jsonify([model.as_dict() for model in models])

@app.route('/models/get', methods=['POST'])
def get_model():
    session = SessionMaker()
    model_id = request.get_json()['id']
    model = session.query(Model).filter_by(id=model_id).first()
    session.close()

    return jsonify(model.as_dict())

@app.route('/models/create', methods=['POST'])
def create_model():
    session = SessionMaker()
    data = request.get_json()
    model = Model(**data)
    session.add(model)
    

    data = session.query(Data).filter_by(id=model.data_id).first()
    if data:
        problem = session.query(Problem).filter_by(id=data.problem_id).first()
        if problem:
            problem.submissions_count += 1
    session.commit()
    session.refresh(model)

    session.close()

    response = requests.post(VALIDATOR_URL + "models", json=debug_json(model.as_dict()), headers={"Content-Type": "application/json"})
    data = model.as_dict()
    data["hash"] = response.text
    return jsonify(data)

@app.route('/models/update', methods=['POST'])
def update_model():
    session = SessionMaker()
    data = request.get_json()
    model = session.query(Model).filter_by(id=data['id']).first()
    for key in data:
        setattr(model, key, data[key])
    session.commit()
    session.close()

    return jsonify(model.as_dict())

@app.route('/models/delete', methods=['POST'])
def delete_model():
    session = SessionMaker()
    model_id = request.get_json()['id']
    model = session.query(Model).filter_by(id=model_id).first()
    session.delete(model)

    data = session.query(Data).filter_by(id=model.data_id).first()
    if data:
        problem = session.query(Problem).filter_by(id=data.problem_id).first()
        if problem:
            problem.submissions_count += 1
    session.commit()

    session.close()

    return jsonify(model.as_dict())

# Result routes
@app.route('/results', methods=['POST'])
def results():
    session = SessionMaker()
    results = session.query(Result).all()
    session.close()

    return jsonify([result.as_dict() for result in results])

@app.route('/results/get', methods=['POST'])
def get_result():
    session = SessionMaker()
    result_id = request.get_json()['id']
    result = session.query(Result).filter_by(id=result_id).first()
    session.close()

    return jsonify(result.as_dict())


@app.route('/results/create', methods=['POST'])
def create_result():
    session = SessionMaker()
    data = request.get_json()
    result = Result(**data)
    session.add(result)
    session.commit()

    session.refresh(result)
    session.close()

    response = requests.post(VALIDATOR_URL + "results", json=debug_json(result.as_dict()), headers={"Content-Type": "application/json"})
    data = result.as_dict()
    data["hash"] = response.text
    return jsonify(data)

@app.route('/results/update', methods=['POST'])
def update_result():
    session = SessionMaker()
    data = request.get_json()
    result = session.query(Result).filter_by(id=data['id']).first()
    for key in data:
        setattr(result, key, data[key])
    session.commit()
    session.close()

    return jsonify(result.as_dict())

@app.route('/results/delete', methods=['POST'])
def delete_result():
    session = SessionMaker()
    result_id = request.get_json()['id']
    result = session.query(Result).filter_by(id=result_id).first()
    session.delete(result)
    session.commit()
    session.refresh(result)
    session.close()

    return jsonify(result.as_dict())