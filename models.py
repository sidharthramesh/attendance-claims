from flask_app import db

class Department(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(40))
    classes = db.relationship('Period',backref='department',lazy='dynamic')
    username = db.Column(db.String(40))
    password = db.Column(db.String(40))
    claims = db.relationship('Claim',backref = 'department',lazy='dynamic')
    def __repr__(self):
        return "<department {}>".format(self.name)

class Period(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    batch_id = db.Column(db.Integer, db.ForeignKey('batch.id'))
    name = db.Column(db.String(40))
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    day = db.Column(db.Integer)
    def __repr__(self):
        return "<{name}  {start} to {end}>".format(name=self.name,start=self.start_time,end=self.end_time)

class Batch(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(40))
    classes = db.relationship('Period',backref='batch',lazy='dynamic')
    def __repr__(self):
        return "<batch {}>".format(self.name)

class Claim(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    event = db.Column(db.String(40))
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    date = db.Column(db.Date)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    period = db.Column(db.String(40))
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    approval_js = db.Column(db.Integer, default = 0)
    approval_office = db.Column(db.Integer, default = 0)
    approval_dept = db.Column(db.Integer, default = 0)
    #semester = db.Column(db.Integer)
    def __repr__(self):
        approval_status = self.approval_js + self.approval_office +self.approval_dept
        return "<{date} {event} for {user} {department}. Approval status: {approval}>".format(date = self.date, event = self.event, user = self.user, approval=approval_status,department = self.department)

class User(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    roll_no = db.Column(db.Integer)
    name = db.Column(db.String(40))
    email = db.Column(db.String(40))
    serial = db.Column(db.Integer)
    claims = db.relationship('Claim',backref='user',lazy='dynamic')
    def __repr__(self):
        return "<user {}>".format(self.name)
