from flask import request, Flask, render_template,jsonify, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
import dateutil.parser, os
from config import SQLALCHEMY_DATABASE_URI
from flask_migrate import Migrate
import flask_excel as excel
from datetime import date
from flask_assets import Environment, Bundle
from departments import depts
from io import StringIO
import pandas as pd
app = Flask(__name__,static_url_path='/static')
app.config["DEBUG"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.secret_key = os.urandom(12)
assets = Environment(app)

css = Bundle(
    'css/loginstyle.css',
    'css/styles.css',
    output='css/min.css'
)
assets.register('css_all', css)

js = Bundle(
    'js/script_index.js',
    filters='rjsmin',
    output='js/app.js'
)
assets.register('js_all', js)

js_list = Bundle(
    'js/script_list.js',
    filters='rjsmin',
    output='js/list.js'
)
assets.register('js_list', js_list)

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
    app.logger.info("Sending email...")
    link= 'https://www.youtube.com/watch?v=CMNry4PE93Y'
    link_text= "Don't click on me"
    text = """Hey yo {name},\n This be the confirmation that we've recieved your claims. We've attached the excel file with this mail.\nCheck if you've sent the correct details or keep it as a souvenir. You can also check your real-time approval status at http://attendance-claims.appspot.com/login. \n\nHave an awesome day! \nMade for u by Stu (Simplyfying Things For You)\n\n¯\_(ツ)_/¯""".format(name = user.name,)
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
def insert_classes(string,all_depts):
    app.logger.info(string)
    depts = all_depts.splitlines()
    batches = string.decode().split('\r\n,,,,,\r\n')
    batches_new = [batch[1:] if batch[0]=='\n' else batch for batch in batches]
    batches = batches_new
    app.logger.info(batches)
    timetables = {}
    no_batches = False
    for table in batches:
        batch = table.splitlines()[0].split(',')[0]
        t =pd.read_csv(StringIO(table))
        t = t[t.columns[1:]]
        t = t.transpose().to_dict()
        timetables[batch] = t
    sem_index = {batch.name:int(batch.semester) for batch in Batch.query.all()}
    if len(sem_index.keys()) < 7:
        no_batches = True
        sem_index = {'2nd Year Batch A':4, '2nd Year Batch B':4,'3rd Year Batch A':6, '3rd Year Batch B':6, '4th Year Batch A':8, '4th Year Batch B':8, '1st Year Batch A':2, '1st Year Batch B':2}
    for batch,table in timetables.items():

        app.logger.info(batch)
        batch_obj = Batch.query.filter(Batch.name == batch).first()
        if no_batches:
            batch_obj = Batch(name = batch, semester = int(sem_index[batch]))
            db.session.add(batch_obj)
            db.session.commit()
        for day,classes in table.items():
            for time,period in classes.items():
                if isinstance(period, str):
                    [start_time,end_time] = [dateutil.parser.parse(a).time() for a in time.split(' to ')]
                    department = None
                    for dep in depts:
                        if dep in period:
                            department = dep
                            break
                    print("{} {}".format(period,department))
                    department = Department.query.filter_by(name = department).first()
                    p = Period(name = period, start_time = start_time, end_time=end_time, batch = batch_obj, day = int(day+1),department = department)
                    print(p)
                    db.session.add(p)
                    db.session.commit()
def delete_all(Object):
    classes = Object.query.all()
    for period in classes:
        db.session.delete(period)
    try:
        db.session.commit()
    except:
        db.session.rollback()
        raise

def reinsert_classes(string,all_depts):
    delete_all(Period)
    #delete_all(Batch)
    insert_classes(string,all_depts)
    return

def get_schedule(date,batch):
    day = dateutil.parser.parse(date).weekday()+1
    app.logger.info(day)
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
def get_allclaims(*fil,approved = True,department = False):
    """formatter claims object to sand as json"""
    if approved:
        non_disapproved = Claim.query.filter(Claim.dissapprove == 0)
    else:
        non_disapproved = Claim.query.filter(Claim.dissapprove == 1)
    new_claims = non_disapproved.filter(*(fil))
    if not department:
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
    if department:
        all_batches = [claim.batch for claim in new_claims.group_by(Claim.batch_id)]
        claims = {}
        for batch in all_batches:
            batchdict = {}
            batchclaims = new_claims.filter(Claim.batch == batch)
            users = [claim.user for claim in batchclaims.group_by(Claim.user_id)]
            for user in users:
                userclaims = batchclaims.filter(Claim.user == user)
                userclaims = parse_claims_list(userclaims)
                batchdict[user.serial] = userclaims
            claims[batch.name] = batchdict
        return claims
def format_claims(ids):
    claims_objs = Claim.query.filter(Claim.id.in_(ids))
    claims = [['Serial', 'Roll no','Name','Date','Classes Missed','Time','Event','Semester']]
    for claim in claims_objs:
        c = [claim.user.serial,claim.user.roll_no,claim.user.name,claim.date.strftime('%d-%B-%y'),claim.period,'{} to {}'.format(get_12hr(claim.start_time),get_12hr(claim.end_time)),claim.event,claim.batch.semester]
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
@app.route('/',methods = ['GET'])
def landing():
    return render_template('landing.html')
@app.route('/claim',methods = ['GET','POST'])
def index():
    return render_template('index.html')
@app.route('/changeclass', methods = ['GET','POST'])
def form():
    if session.get('user') == 'jointsec':
        if request.method == 'GET':
            return render_template('changeclass.html')

        if request.method == 'POST':
            f = request.files['data_file']
            csv_string = f.read()
            app.logger.info(reinsert_classes(csv_string,depts))
            app.logger.info(Period.query.all())
            flash("Classes updated!")
            return redirect('/dashboard')
    else:
        return redirect('/dashboard')

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
            if request.args.get('filter') == 'disapproved':
                return jsonify(get_allclaims(approved = False))
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
        non_disapproved = dep.claims.filter(Claim.dissapprove == 0)
        if request.method == 'GET':
            if request.args.get('filter') == 'all':
                return jsonify(get_allclaims(Claim.department == dep,Claim.approval_office == 1, department = True))
            if request.args.get('filter') == 'approved':
                return jsonify(get_allclaims(Claim.department == dep,Claim.approval_dept == 1, department = True))
            else:
                return jsonify(get_allclaims(Claim.department == dep,Claim.approval_office==1, department = True))
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
    all_claims = False
    if session.get('student'):
        return render_template('list.html',admin = False, uname = User.query.get(session.get('student')).name)
    if session.get('user'):
        u = session.get('user')
        if u == 'jointsec':
            uname = 'Joint Seceratary'
        elif u == 'office':
            uname = 'Office'
        else:
            uname = Department.query.get(u).name
        app.logger.info(uname)
        if request.args.get('claims') == 'approved':
            all_claims = True
        return render_template('list.html',admin = True, uname = uname,all_claims = all_claims)
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
    if ids[0] == '':
        return 'None'
    ids = [int(id) for id in ids]
    app.logger.info(ids)
    claims = format_claims(ids)
    app.logger.info(claims)
    return excel.make_response_from_array(claims, file_type = "csv", file_name="Claims_on_{}".format(str(date.today())))
    #return render_template('table.html',claims = claims)
@app.route('/changepassword',methods = ['GET','POST'])
def change_password():

    #app.logger.info(user)
    if request.method == 'GET':
        user = session.get('user')
        if user:
            return render_template('changepwd.html',status = None)
        else:
            return redirect('/login')
    if request.method == 'POST':
        user = session.get('user')
        if user == 'jointsec':
            app.logger.info('inside jointsec')
            u = Special.query.filter(Special.username == session['username']).first()
            app.logger.info(u.password)
        elif user == 'office':
            u = Special.query.filter(Special.username == 'office').first()
        elif user:
            u = Department.query.get(user)
        app.logger.info(u)
        app.logger.info(request.form['newpass'] + '-----'+ request.form['confirm'])
        if request.form['newpass'] == request.form['confirm']:
            #app.logger.info(request.form['oldpass'] + '-----'+ request.form['confirm'])
            if request.form['oldpass'] == u.password:
                app.logger.info(u.password)
                u.password = request.form['newpass']
                try:
                    db.session.commit()
                except:
                    db.session.rollback()
                    raise
                flash("Password successfully changed!")
                return redirect('/dashboard')
            return render_template('changepwd.html',status = 'Wrong old password')
        return render_template('changepwd.html',status = "New passwords didn't match")

@app.route('/changesem',methods = ['GET','POST'])
def change_sem():
    if session.get('user') == 'jointsec':
        if request.method == 'GET':
            batches = Batch.query.all()
            return render_template('batchchange.html',batches = batches)
        if request.method == 'POST':
            for batch_id,semester in request.form.items():
                b = Batch.query.get(batch_id)
                try:
                    b.semester = int(semester)
                except:
                    pass
            try:
                db.session.commit()
            except:
                db.session.rollback()
                raise
            flash("Semesters have been changed!")
            return redirect('/dashboard')
    else:
        flash('Only Joint Seceratary can do that')
        return redirect('/dashboard')
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
            session['username'] = request.form['username']
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
    return "What are you doing with life bro?", 404
