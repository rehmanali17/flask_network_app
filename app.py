from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#init db
db = SQLAlchemy(app)


# Second Approach
Base = automap_base()
Base.prepare(db.engine, reflect=True)
Devices = Base.classes.devices
# Incident = Base.classes.incident
# Users = Base.classes.users

@app.route('/')
def login():
   return render_template('login.html')


@app.route('/register')
def register():
   return render_template('register.html')


@app.route('/devices')
def incidents():
    devices = db.session.query(Devices).all()
    return render_template('devices.html', devices=devices)

if __name__ == "__main__":
    app.run(debug=True)