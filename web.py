import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import configparser

config = configparser.ConfigParser()
config.read('config_local.ini')

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_DATABASE_URI'] = config['DATABASE']['STRING']
db = SQLAlchemy(app)

class Data(db.Model):
    __tablename__ = 'data'
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(300))
    type = db.Column(db.String(100))
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, value, name, type):
        self.value = value
        self.name = name
        self.type = type
        
    def __repr__(self):
        return "<Data(value='%s', name='%s', type='%s', date='%s')>" % (self.value, self.name, self.type, self.date)


@app.route('/')#,methods=['POST','GET']
def index():
    value = "test"
    name = "test"
    type = "test"
        
    values = Data(value, name, type)
    db.session.add(values)
    db.session.commit()
            
    return "Hello, World"


if __name__ == "__main__":
    app.run(debug=True)
    app.run(host = '0.0.0.0', post = 5000)
