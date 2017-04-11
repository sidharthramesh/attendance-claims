from flask_app import *
for department in ['Microbiology',]:
    Department(name = 'Microbiology',username = 'admin', password = 'admin123')
batcha = Batch(name = '4th Sem Batch a')
db.session.add(micro)
db.session.add(batcha)
db.session.commit()
from datetime import date, time
mon = Day(name = 'Monday')
db.session.add(mon)
db.session.commit()

for day in ['Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']:
    db.session.add(Day(name = day))
db.session.commit()
microtheory = Period(name ='Microbiology Lecture', start_time = time(9), end_time = time(12), department=micro,day=mon)
db.session.add(microtheory)
db.session.commit()

sid = User(roll_no='150101312',name='Sidharth',email='tornadoalert@gmail.com',serial='104')
db.session.add(sid)
db.session.commit()

testclaim = Claim(user=sid,date = date.today(),period=microtheory,department=micro)
db.session.add(testclaim)
db.session.commit()

testclaim.approval_dept = 1
db.session.commit()
print(micro.claims.first())
