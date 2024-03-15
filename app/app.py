import os

import dotenv
import psycopg2

dotenv.load_dotenv()


while True:
    try:
        conn = psycopg2.connect(
            host=os.environ['POSTGRES_HOST'],
            database=os.environ['POSTGRES_DB'],
            user=os.environ['POSTGRES_USER'],
            password=os.environ['POSTGRES_PASSWORD']
        )
        print("Connected to database")
        break
    except Exception as e:
        print(e)
        continue

print(conn)
from flask import Flask, render_template, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

database_uri = 'postgresql+psycopg2://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
    dbuser=os.environ['POSTGRES_USER'],
    dbpass=os.environ['POSTGRES_PASSWORD'],
    dbhost=os.environ['POSTGRES_HOST'],
    dbname=os.environ['POSTGRES_DB']
)

app = Flask(__name__)
app.config.update(
    SQLALCHEMY_DATABASE_URI=database_uri,
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

# initialize the database connection
db = SQLAlchemy(app)

# initialize database migration management
migrate = Migrate(app, db)

@app.route('/')
def view_registered_guests():
    from models import Guest
    guests = Guest.query.all()
    return render_template('guest_list.html', guests=guests)


@app.route('/register', methods=['GET'])
def view_registration_form():
    return render_template('guest_registration.html')


@app.route('/register', methods=['POST'])
def register_guest():
    from models import Guest
    name = request.form.get('name')
    email = request.form.get('email')

    guest = Guest(name, email)
    db.session.add(guest)
    db.session.commit()

    return render_template(
        'guest_confirmation.html', name=name, email=email)
