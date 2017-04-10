from flask import request, Flask, render_template,jsonify
from flask_sqlalchemy import SQLAlchemy
import dateutil.parser
from config import SQLALCHEMY_DATABASE_URI
from flask_migrate import Migrate
app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Department(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String)
    classes = db.relationship('Period',backref='department',lazy='dynamic')
    username = db.Column(db.String)
    password = db.Column(db.String)
    claims = db.relationship('Claim',backref = 'department',lazy='dynamic')
    def __repr__(self):
        return "<department {}>".format(self.name)

class Period(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    batch_id = db.Column(db.Integer, db.ForeignKey('batch.id'))
    name = db.Column(db.String)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    day_id = db.Column(db.Integer,db.ForeignKey('day.id'))
    claims = db.relationship('Claim',backref='period',lazy='dynamic')
    def __repr__(self):
        return "<{name}  {start} to {end}>".format(name=self.name,start=self.start_time,end=self.end_time)

class Batch(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String)
    classes = db.relationship('Period',backref='batch',lazy='dynamic')
    def __repr__(self):
        return "<batch {}>".format(self.name)

class Day(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String)
    classes = db.relationship('Period',backref='day',lazy='dynamic')
    def __repr__(self):
        return "<day {}>".format(self.name)

class Claim(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    date = db.Column(db.Date)
    period_id = db.Column(db.Integer, db.ForeignKey('period.id'))
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    approval_js = db.Column(db.Integer, default = 0)
    approval_office = db.Column(db.Integer, default = 0)
    approval_dept = db.Column(db.Integer, default = 0)

    def __repr__(self):
        approval_status = self.approval_js + self.approval_office +self.approval_dept
        return "<{date} for {user}. Approval status: {approval}>".format(date = self.date, user = self.user, approval=approval_status)
class User(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    roll_no = db.Column(db.Integer)
    name = db.Column(db.String)
    email = db.Column(db.String)
    serial = db.Column(db.Integer)
    claims = db.relationship('Claim',backref='user',lazy='dynamic')
    def __repr__(self):
        return "<user {}>".format(self.name)
def get_schedule(date, batch = 'batch_a'):
    classes = {'batch_a':{0: {'8 AM to 9 AM': 'Microbiology', '9:30 AM to 12 Noon': 'Postings', '2 PM to 3 PM': 'Pathology', '3 PM to 4 PM': 'Microbiology practicals', '4 PM to 5 PM': 'nan'}, 1: {'8 AM to 9 AM': 'Medicine', '9:30 AM to 12 Noon': 'Postings', '2 PM to 3 PM': 'Pharmacology', '3 PM to 4 PM': 'Forensic Medicine CBL', '4 PM to 5 PM': 'Forensic Medicine Practicals'}, 2: {'8 AM to 9 AM': 'Community Medicine', '9:30 AM to 12 Noon': 'Postings', '2 PM to 3 PM': 'Pathology', '3 PM to 4 PM': 'Pathology practicals', '4 PM to 5 PM': 'nan'}, 3: {'8 AM to 9 AM': 'Pharmacology', '9:30 AM to 12 Noon': 'Postings', '2 PM to 3 PM': 'Microbiology', '3 PM to 4 PM': 'Pharmacology practicals', '4 PM to 5 PM': 'nan'}, 4: {'8 AM to 9 AM': 'Surgery', '9:30 AM to 12 Noon': 'Postings', '2 PM to 3 PM': 'Pathology', '3 PM to 4 PM': 'Community Medicine practicals', '4 PM to 5 PM': 'nan'}, 5: {'8 AM to 9 AM': 'Forensic Medicine/Microbiology', '9:30 AM to 12 Noon': 'Postings', '2 PM to 3 PM': 'Pharmacology', '3 PM to 4 PM': 'Bio Ethics*', '4 PM to 5 PM': 'nan'}},'batch_b':{0: {'8 AM to 9 AM': 'Microbiology', '9:30 AM to 12 Noon': 'Postings', '2 PM to 3 PM': 'Pathology', '3 PM to 4 PM': 'Pathology practicals', '4 PM to 5 PM': 'nan'}, 1: {'8 AM to 9 AM': 'Medicine', '9:30 AM to 12 Noon': 'Postings', '2 PM to 3 PM': 'Pharmacology', '3 PM to 4 PM': 'Microbiology practicals', '4 PM to 5 PM': 'nan'}, 2: {'8 AM to 9 AM': 'Community Medicine', '9:30 AM to 12 Noon': 'Postings', '2 PM to 3 PM': 'Pathology', '3 PM to 4 PM': 'Pharmacology practicals', '4 PM to 5 PM': 'nan'}, 3: {'8 AM to 9 AM': 'Pharmacology', '9:30 AM to 12 Noon': 'Postings', '2 PM to 3 PM': 'Microbiology', '3 PM to 4 PM': 'Forensic Medicine CBL', '4 PM to 5 PM': 'Forensic Medicine Practicals'}, 4: {'8 AM to 9 AM': 'Surgery', '9:30 AM to 12 Noon': 'Postings', '2 PM to 3 PM': 'Pathology', '3 PM to 4 PM': 'Community Medicine practicals', '4 PM to 5 PM': 'nan'}, 5: {'8 AM to 9 AM': 'Forensic Medicine/Microbiology', '9:30 AM to 12 Noon': 'Postings', '2 PM to 3 PM': 'Pharmacology', '3 PM to 4 PM': 'Bio Ethics*', '4 PM to 5 PM': 'nan'}}}
    classes = classes[batch]
    if get_day(date) == 6:
        return
    return classes[get_day(date)]
def get_day(date):
    d = dateutil.parser.parse(date)
    return int(d.weekday())
@app.route('/',methods = ['GET','POST'])
def index():
    if request.method == 'POST':
        date = request.form['date']
        batch = request.form['batch']
        return jsonify(get_schedule(date,batch))
    return render_template('index.html',heading = 'Hello there!')

@app.route('/classdata',methods = ['GET'])
def class_data():
    """Request class data with params date=(2017-12-31) and batch=batch_a"""
    date = request.args.get('date')
    batch = request.args.get('batch')
    return jsonify(get_schedule(date,batch))

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return "Not found page", 404
