import pandas as pd
from dateutil import parser
from io import StringIO

from flask_app import *
from models import *

with open('timetable_NEW.csv','r') as f:
    string = f.read()

batches = string.split(',,,,,')

batches_new = [batch[1:] if batch[0]=='\n' else batch for batch in batches]

batches = batches_new

depts = """Anatomy
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
Orthopaedics"""

depts = depts.splitlines()

timetables = {}
for table in batches:
    batch = table.splitlines()[0].split(',')[0]
    t =pd.read_csv(StringIO(table))
    t = t[t.columns[1:]]
    t = t.transpose().to_dict()
    timetables[batch] = t



print(timetables.keys())

for dep in depts:
    com = dep.split(' ')[0].lower()
    obj = Department(name = dep, username = com, password = com+'123password')
    db.session.add(obj)
db.session.commit()

Department.query.all()

for batch,table in timetables.items():
    batch_obj = Batch(name = batch)
    db.session.add(batch_obj)
    db.session.commit()
    for day,classes in table.items():
        for time,period in classes.items():
            if isinstance(period, str):
                [start_time,end_time] = [parser.parse(a).time() for a in time.split(' to ')]
                department = None
                for dep in depts:
                    if dep in period:
                        department = dep
                        break
                print("{} {}".format(period,department))
                department = Department.query.filter_by(name = department).first()
                p = Period(name = period, start_time = start_time, end_time=end_time, batch = batch_obj, day = int(day+1),department = department)
                db.session.add(p)
                db.session.commit()

# Delete ALL!!!
#for i in reversed(db.metadata.sorted_tables):
#    db.session.execute(i.delete())
#    db.session.commit()
