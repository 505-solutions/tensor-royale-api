
from database import SessionMaker, database_uri, init_db
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from models.data import Data
from models.model import Model
from models.problem import Problem
from models.user import User

app = Flask(__name__)
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

    return jsonify(problem.as_dict()) 

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
    session = SessionMaker()
    data = session.query(Data).all()
    session.close()

    return jsonify([datum.as_dict() for datum in data])

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
    session.commit()

    session.refresh(datum)

    session.close()

    return jsonify(datum.as_dict())

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
    session.commit()

    session.refresh(model)

    session.close()

    return jsonify(model.as_dict())

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
    session.commit()
    session.close()

    return jsonify(model.as_dict())