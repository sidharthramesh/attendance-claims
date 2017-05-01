import pandas as pd
from dateutil import parser
from io import StringIO

from flask_app import *
from models import *
from departments import depts

def main():
    db.create_all()
    sem_index = {'2nd Year Batch A':4, '2nd Year Batch B':4,'3rd Year Batch A':6, '3rd Year Batch B':6, '4th Year Batch A':8, '4th Year Batch B':8, '1st Year Batch A':2, '1st Year Batch B':2}


def insert_depts(all_depts):
    depts = deptarts.splitlines()
    for dep in depts:
        com = dep.split(' ')[0].lower()
        obj = Department(name = dep, username = com, password = com+'123password')
        db.session.add(obj)
    db.session.commit()

def insert_classes(string,all_depts):
    depts = deptarts.splitlines()
    batches = string.split(',,,,,')
    batches_new = [batch[1:] if batch[0]=='\n' else batch for batch in batches]
    batches = batches_new
    timetables = {}
    for table in batches:
        batch = table.splitlines()[0].split(',')[0]
        t =pd.read_csv(StringIO(table))
        t = t[t.columns[1:]]
        t = t.transpose().to_dict()
        timetables[batch] = t

    for batch,table in timetables.items():
        batch_obj = Batch(name = batch, semester = int(sem_index[batch]))
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
def delete_classes():
    classes = Period.query.all()
    for period in classes:
        db.session.delete(period)
    try:
        db.session.commit()
    except:
        db.session.rollback()
        raise
def reinsert_classes(string,all_depts):
    delete_classes()
    insert_classes(string,all_depts)
    return

def special_insert():
    for user in ['jointsec1','jointsec2']:
        obj = Special(name = 'jointsec', username = user,password = user+str(123))
        db.session.add(obj)
    db.session.commit()
    obj = Special(name = 'office', username = 'office' ,password = 'office'+str(123))
    db.session.add(obj)
    db.session.commit()
if __name__ == '__main__':
    main()
    with open('timetable_NEW.csv','r') as f:
        string = f.read()
    all_depts = depts
    if input("Insert depts?").lower() in ['y','yes']:
        insert_depts(all_depts)
    if input("Insert timetable?").lower() in ['y','yes']:
        insert_classes(string,depts)
    if input("Insert special logins?").lower() in ['y','yes']:
        special_insert()
