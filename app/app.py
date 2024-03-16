
from database import SessionMaker, database_uri, init_db
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
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

@app.route('/')
def view_registered_guests():
    # create a session to manage the connection to the database 
    session = SessionMaker() 
    
    # query the users table 
    users = session.query(User).all() 
    print(users) 

    session.close()
    return jsonify([u.__repr__() for u in users])

@app.route('/add', methods=['GET'])
def register_user():
    wallet = request.args.get('wallet')
    title = request.args.get('title')
    
    session = SessionMaker()

    user = User(wallet=wallet, title=title)
    session.add(user)
    session.commit()

    session.close()
    return jsonify("User added")



# @app.route('/register', methods=['GET'])
# def view_registration_form():
#     return render_template('guest_registration.html')


# @app.route('/register', methods=['POST'])
# def register_guest():
#     from models import Guest
#     name = request.form.get('name')
#     email = request.form.get('email')

#     guest = Guest(name, email)
#     db.session.add(guest)
#     db.session.commit()

#     return render_template(
#         'guest_confirmation.html', name=name, email=email)
