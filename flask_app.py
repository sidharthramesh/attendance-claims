from flask import request, Flask, render_template,jsonify
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
all_depts = """Anatomy
Physiology
Biochemistry
Community Medicine
Pathology
Pharmacology
Microbiology
Forensic Medicine
Medicine
ENT
OBG
Opthalmology
Surgery
Paediatrics
Pulmonary Medicine
Orthopaedics""".splitlines()
posting_depts = """Community Medicine
Medicine
ENT
OBG
Opthalmology
Surgery
Paediatrics
Pulmonary Medicine
Orthopaedics""".splitlines()

def get_schedule(date,batch):
    day = dateutil.parser.parse(date).weekday()+1
    return Period.query.filter_by(day=day, batch = Batch.query.filter_by(name=batch).first()).order_by(Period.start_time).all()
def process_claim(data):
    pass
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
        user = User.query.filter_by(roll_no=int(data['rollNumber'])).first()
        new_user = False
        if user == None:

            new_user = True
            user = User(roll_no = int(data['rollNumber'], name = data['name'],email = data['email'], serial = data['serialNumber']))
            app.logger.info("User is {}".user.name)
            #db.add(u)
            #db.commit()
        for period in data['selectedClasses']:
            department = Department.query.filter_by(name = period['department']).first()
            claim_obj = Claim(event = data['event'], user = user, date = period['date'], start_time=period['startTime'], end_time = period['endTime'],department = department )
            app.logger.info(str(claim_obj))
            #db.add(claim_obj)
            #db.commit()
@app.route('/status_check',methods = ['GET','POST'])
def status_check():
    pass
@app.route('/login',methods = ['GET','POST'])
def login():
    pass
@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return "Not found page", 404
