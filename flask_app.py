from flask import request, Flask, render_template,jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
import dateutil.parser
from config import SQLALCHEMY_DATABASE_URI
from flask_migrate import Migrate
app = Flask(__name__,static_url_path='/static')
app.config["DEBUG"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
db = SQLAlchemy(app)
migrate = Migrate(app, db)
from models import *
from departments import depts, posting_depts
all_depts = depts.splitlines()
posting_depts = posting_depts.splitlines()

def get_schedule(date,batch):
    day = dateutil.parser.parse(date).weekday()+1
    return Period.query.filter_by(day=day, batch = Batch.query.filter_by(name=batch).first()).order_by(Period.start_time).all()
def process_claim(data):
    pass
def get_time(string):
    d = dateutil.parser.parse(string)
    return d.time()
def get_date(string):
    d = dateutil.parser.parse(string)
    return d.date()
@app.route('/',methods = ['GET','POST'])
def index():
    return render_template('index.html')
@app.route('/classdata',methods = ['GET','POST'])
def class_data():
    """Request class data with params date=(2017-12-31) and batch=batch_a"""
    if request.method == 'GET':
        date = request.args.get('date')
        batch = request.args.get('batch')
        if date and batch:
            classes = []
            for period in get_schedule(date,batch):
                class_obj = {'id':period.id, 'name' : period.name, 'start_time':str(period.start_time), 'end_time':str(period.end_time),'department':all_depts,'date':date}
                if period.name == 'Postings':
                    class_obj['department'] = posting_depts
                if not period.department == None:
                    class_obj['department'] = period.department.name
                classes.append(class_obj)
            return jsonify(classes)
    if request.method == 'POST':
        data = request.json
        app.logger.info(str(data))
        user = User.query.filter_by(roll_no=int(data['rollNumber'])).first()
        new_user = False
        if user == None:

            new_user = True
            user = User(roll_no = int(data['rollNumber']), name = data['name'],email = data['email'], serial = data['serialNumber'])
            #app.logger.info("User is {}".format(user.name))
            try:
                db.session.add(user)
                db.session.commit()
            except:
                db.session.rollback()
                raise

        for period in data['selectedClasses']:
            department = Department.query.filter_by(name = period['department']).first()
            claim_obj = Claim(event = data['event'], user = user, date = get_date(period['date']), start_time=get_time(period['start_time']), end_time = get_time(period['end_time']),department = department, approval_js =0,approval_office =0, approval_dept = 0)
            app.logger.info(str(claim_obj))
            try:
                db.session.add(claim_obj)
                db.session.commit()
            except:
                db.session.rollback()
                return jsonify({"status":"failed"})
                raise
        return jsonify({"status":"success"})

@app.route('/status_check',methods = ['GET','POST'])
def status_check():
    pass
@app.route('/login',methods = ['GET','POST'])
def login():
    return "Login page work in progress"
@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return "Not found page", 404
