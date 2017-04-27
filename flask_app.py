from flask import request, Flask, render_template,jsonify, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
import dateutil.parser, os
from config import SQLALCHEMY_DATABASE_URI
from flask_migrate import Migrate
import flask_excel as excel
from datetime import date
app = Flask(__name__,static_url_path='/static')
app.config["DEBUG"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.secret_key = os.urandom(12)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
from models import *
from departments import depts, posting_depts
all_depts = depts.splitlines()
posting_depts = posting_depts.splitlines()
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from email.utils import formataddr
from email.header import Header

def sendmail(user, attachment, event):
    link= 'https://www.youtube.com/watch?v=CMNry4PE93Y'
    link_text= 'Just Click'
    text = """Hey yo {name}. This be the confirmation that we've recieved your claims. We've attached the excel file with this mail.\nCheck if you've sent the correct details or keep it as a souvenir. \n\nHave an awesome day! \nMade for u by Stu (Simplyfying Things For You)\n\n¯\_(ツ)_/¯""".format(name = user.name,)
    msg = MIMEMultipart()
    msg['Subject'] = '{} Claims'.format(event)
    msg['From'] = formataddr((str(Header('Simplified Claims', 'utf-8')), 'stu.checks.mail@gmail.com'))
    msg.attach(MIMEText(text))
    msg.attach(MIMEText(u'<a href="{link}">{link_text}</a>'.format(link=link,link_text=link_text),'html'))
    filename = '{}_claims.csv'.format(event.split(' ')[0].lower())
    part = MIMEApplication(attachment, Name = filename)
    part['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
    msg.attach(part)
    mailer = smtplib.SMTP('smtp.gmail.com:587')
    mailer.starttls()
    mailer.login('stu.checks.mail','YouOweMe5bux')
    mailer.sendmail('stu.checks.mail@gmail.com',user.email,msg.as_string())
    mailer.close()
    return

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
    c['Roll_no'] = claim.user.roll_no
    c['Name'] = claim.user.name
    c['Period'] = claim.period
    c['Time'] = "{} to {}".format(get_12hr(claim.start_time),get_12hr(claim.end_time))
    c['status'] = {'js':claim.approval_js,'office': claim.approval_office,'dept':claim.approval_dept}
    c['dissapproved'] = claim.dissapprove
    return c
def parse_claims_list(claims):
    return [parse_claim(claim) for claim in claims]
def get_allclaims(*fil):
    """formatter claims object to sand as json"""
    non_disapproved = Claim.query.filter(Claim.dissapprove == 0)
    new_claims = non_disapproved.filter(*(fil))
    all_events = [claim.event for claim in new_claims.group_by(Claim.event)]
    claims = {}
    for event in all_events:
        eventdict = {}
        eventclaims = new_claims.filter(Claim.event == event)
        users = [claim.user for claim in eventclaims.group_by(Claim.user_id)]
        for user in users:
            userclaims = eventclaims.filter(Claim.user == user)
            userclaims = parse_claims_list(userclaims)
            eventdict[user.name] = userclaims
        claims[event] = eventdict
    return claims
def format_claims(ids):
    claims_objs = get_new_by_ids(ids)
    claims = [['Serial', 'Roll no','Name','Date','Classes Missed','Time','Event','Semester']]
    for claim in claims_objs:
        c = [claim.user.serial,claim.user.roll_no,claim.user.name,claim.date,claim.period,'{} to {}'.format(get_12hr(claim.start_time),get_12hr(claim.end_time)),claim.event,claim.batch.semester]
        claims.append(c)
    return claims
def get_new_by_ids(ids):
    return Claim.query.filter(Claim.id.in_(ids), Claim.approval_js == 0).all()
def get_jsapproved_by_ids(ids):
    return Claim.query.filter(Claim.id.in_(ids), Claim.approval_js == 1).all()
def array_to_csv(array):
    rows = []
    for row in array:
        r = ','.join([str(element) for element in row])
        rows.append(r)
    return '\n'.join(rows)
def js_approve(ids):
    approved = get_new_by_ids(ids)
    app.logger.info(approved)
    for claim in approved:
        claim.approval_js = 1
        print('JS Approved {}'.format(claim))
        try:
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({"status":False})
            raise
    return jsonify({"status":True})
def disapprove(ids):
    dissapproved = Claim.query.filter(Claim.id.in_(ids)).all()
    for claim in dissapproved:
        claim.dissapprove = 1
        try:
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({"status":False})
    return jsonify({"status":True})

def office_approve(ids):
    approved = get_jsapproved_by_ids(ids)
    for claim in approved:
        claim.approval_office = 1
        try:
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({"status":False})
            raise
    return jsonify({"status":True})
def department_approve(ids):
    approved = get_jsapproved_by_ids(ids)
    for claim in approved:
        claim.approval_dept = 1
        try:
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({"status":False})
            raise
    return jsonify({"status":True})
def department_validate(username,password):
    result = Department.query.filter(Department.username == username).first()
    if result:
        if result.password == password:
            return result
    return None
def student_validate(username,password):
    result = User.query.filter(User.roll_no == username).first()
    if result:
        return result
    return None
def special_validate(username,password):
    result = Special.query.filter(Special.username == username).first()
    if result:
        if result.password == password:
            return result.name
    return None
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
        if data['rollNumber'] == '':
            return jsonify('empty roll no. Cannot process.')
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
            if not any([dept in period['name'] for dept in all_depts]):
                name = period['department']+ ' ' +period['name']
            else:
                name = period['name']
            claim_obj = Claim(dissapprove = 0, period = name ,batch=batch, event = data['event'], user = user, date = get_date(period['date']), start_time=get_time(period['start_time']), end_time = get_time(period['end_time']),department = department, approval_js =0,approval_office =0, approval_dept = 0)
            #app.logger.info(str(claim_obj))
            try:
                db.session.add(claim_obj)
                db.session.commit()
                id_index.append(claim_obj.id)
            except:
                db.session.rollback()
                return jsonify({"status":"failed"})
                raise
        sendmail(user,array_to_csv(format_claims(id_index)),data['event'])
        return jsonify(id_index)
        #return jsonify({"status":"success"})


@app.route('/claims',methods = ['GET','POST'])
def claims_api():
    user = session.get('user')
    if user == 'jointsec':
        #app.logger.info('Jointsec Logged in!')
        if request.method == 'GET':
            if request.args.get('filter') == 'all':
                return jsonify(get_allclaims())
            if request.args.get('filter') == 'approved':
                return jsonify(get_allclaims(Claim.approval_js == 1))
            else:
                return jsonify(get_allclaims(Claim.approval_js == 0))

        if request.method == 'POST':
            app.logger.info('Got POST')
            data = request.json
            action = data['action']
            if action == 'approve':
                app.logger.info(data['ids'])
                return js_approve(data['ids'])
            if action == 'disapprove':
                return disapprove(data['ids'])
    elif user == 'office':
        if request.method == 'GET':
            if request.args.get('filter') == 'all':
                return jsonify(get_allclaims())
            if request.args.get('filter') == 'approved':
                return jsonify(get_allclaims(Claim.approval_office == 1))
            else:
                return jsonify(get_allclaims(Claim.approval_js == 1,Claim.approval_office==0))

        if request.method == 'POST':
            data = request.json
            action = data['action']
            if action == 'approve':
                return office_approve(data['ids'])
            if action == 'disapprove':
                return disapprove(data['ids'])
    elif user:
        dep = Department.query.get(user)
        non_disapproved = dep.query.filter(Claim.dissapprove == 0)
        if request.method == 'GET':
            if request.args.get('filter') == 'all':
                claims_list = non_disapproved.filter(Claim.approval_office==1).all()
                parsed = parse_claims_list(claims_list)
                return jsonify(parsed)
            if request.args.get('filter') == 'approved':
                claims_list = non_disapproved.filter(Claim.approval_dept==1).all()
                parsed = parse_claims_list(claims_list)
                return jsonify(parsed)
            else:
                claims_list = non_disapproved.filter(Claim.approval_office==1,Claim.approval_dept==0).all()
                parsed = parse_claims_list(claims_list)
                return jsonify(parsed)
        if request.method == 'POST':
            data = request.json
            action = data['action']
            if action == 'approve':
                return department_approve(data['ids'])
            if action == 'disapprove':
                return disapprove(data['ids'])
    elif session.get('student'):
        student = User.query.get(session.get('student'))
        if request.method == 'GET':
            claims = student.claims.all()
            return jsonify(parse_claims_list(claims))
        if request.method == 'POST':
            return "Students can't post bitch!"
    else:
        return 'Invalid login'
@app.route('/dashboard', methods = ['GET','POST'])
def dashboard():
    if session.get('student'):
        return render_template('list.html',admin = False, uname = User.query.get(session.get('student')).name)
    if session.get('user'):
        u = session.get('user')
        if u == 'jointsec':
            uname = 'Joint Seceratary'
        else:
            uname = Department.query.get(u).name
        return render_template('list.html',admin = True, uname = uname)
    else:
        return redirect('/login')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')
@app.route('/download', methods = ['GET'])
def make_excel():
    #print(request.json)
    ids = request.args.get('ids')
    ids = ids.split(',')
    ids = [int(id) for id in ids]
    app.logger.info(ids)
    claims = format_claims(ids)

    return excel.make_response_from_array(claims, file_type = "csv", file_name="Claims_on_{}".format(str(date.today())))
    #return render_template('table.html',claims = claims)
@app.route('/login',methods = ['GET','POST'])
def login():
    error = None
    if session.get('user'):
        return redirect('/dashboard')
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        if special_validate(request.form['username'],request.form['password']):
            user = special_validate(request.form['username'],request.form['password'])
            session['user'] = user
            app.logger.info(user)
            return redirect('/dashboard')
        if department_validate(request.form['username'],request.form['password']):
            department = department_validate(request.form['username'],request.form['password'])
            session['user'] = department.id
            return redirect('/dashboard')
        if student_validate(request.form['username'],request.form['password']):
            student = student_validate(request.form['username'],request.form['password'])
            session['student'] = student.id
            return redirect('/dashboard')
        error = "Wrond credentials"
        return render_template('login.html',error = error)
@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return "Not found page", 404
