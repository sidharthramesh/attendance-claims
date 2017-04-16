from flask import request, Flask, render_template,jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import dateutil.parser
from config import SQLALCHEMY_DATABASE_URI
from flask_migrate import Migrate
import flask_excel as excel
from datetime import date
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
def get_12hr(time):
    return time.strftime("%I:%M %p")
def parse_claim(claim):
    c = {}
    c['id'] = claim.id
    c['Event'] = claim.event
    c['Date'] = claim.date
    c['Serial'] = claim.user.serial
    c['Roll no'] = claim.user.roll_no
    c['Name'] = claim.user.name
    c['Period'] = claim.period
    c['Time'] = "{} to {}".format(get_12hr(claim.start_time),get_12hr(claim.end_time))
    return c
def parse_claims_list(claims):
    return [parse_claim(claim) for claim in claims]
def get_all():
    claims = []
    for claim in Claim.query.all():
        c = parse_claim(claim)
        claims.append(c)
    return claims
def get_allnew():
    claims = []
    for claim in Claim.query.filter(Claim.approval_js == 0).all():
        c = parse_claim(claim)
        claims.append(c)
    return claims
def get_new_by_ids(ids):
    return Claim.query.filter(Claim.id.in_(ids), Claim.approval_js == 0).all()
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
                class_obj = {'id':period.id, 'name' : period.name, 'start_time':get_12hr(period.start_time), 'end_time':get_12hr(period.end_time),'department':all_depts,'date':date}
                if period.name == 'Postings':
                    class_obj['department'] = posting_depts
                if not period.department == None:
                    class_obj['department'] = period.department.name
                classes.append(class_obj)
            return jsonify(classes)
    if request.method == 'POST':
        data = request.json
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
        id_index = []
        for period in data['selectedClasses']:
            department = Department.query.filter_by(name = period['department']).first()
            batch = Batch.query.filter_by(name = data['year']+' Year Batch '+data['batch']).first()
            # add semester mapping from data['year']
            claim_obj = Claim(period = period['name'], event = data['event'], user = user, date = get_date(period['date']), start_time=get_time(period['start_time']), end_time = get_time(period['end_time']),department = department, approval_js =0,approval_office =0, approval_dept = 0)
            #app.logger.info(str(claim_obj))
            try:
                db.session.add(claim_obj)
                db.session.commit()
                id_index.append(claim_obj.id)
            except:
                db.session.rollback()
                return jsonify({"status":"failed"})
                raise
        return jsonify(id_index)
        #return jsonify({"status":"success"})

@app.route('/status_check',methods = ['GET','POST'])
def status_check():
    pass
@app.route('/claims',methods = ['GET','POST'])
def view_all():
    if request.method == 'GET':
        f = request.args.get('filter')
        if f == 'all':
            return jsonify(get_all())
        if f == 'new':
            return jsonify(get_allnew())
    if request.method == 'POST':
        data = request.json
        approved = get_new_by_ids(data['ids'])
        if data['auth'] == 'secret_password123':
            for claim in approved:
                claim.approval_js = 1
                try:
                    db.session.commit()
                except:
                    db.session.rollback()
                    return jsonify({"status":"failed"})
                    raise
        return jsonify({"status":"success"})

@app.route('/download', methods = ['POST'])
def make_excel():
    ids = request.json['ids']
    claims_objs = get_new_by_ids(ids)
    claims = [['Serial', 'Roll no','Name','Date','Class','Time','Event','Semester']]
    for claim in claims_objs:
        c = [claim.user.serial,claim.user.roll_no,claim.user.name,claim.date,claim.period,'{} to {}'.format(get_12hr(claim.start_time),get_12hr(claim.end_time)),claim.event,claim.batch.semester]
        claims.append(c)
    return excel.make_response_from_array(claims, "csv", file_name="Claims_on_{}".format(str(date.today())))
    #return render_template('table.html',claims = claims)
@app.route('/login',methods = ['GET','POST'])
def login():
    return "Login page work in progress"
@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return "Not found page", 404
