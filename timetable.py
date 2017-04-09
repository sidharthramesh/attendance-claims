import dateutil.parser
def get_schedule(date, batch):
    classes = {'batch_a':{0: {'8 AM to 9 AM': 'Microbiology', '9:30 AM to 12 Noon': 'Postings', '2 PM to 3 PM': 'Pathology', '3 PM to 4 PM': 'Microbiology practicals', '4 PM to 5 PM': 'nan'}, 1: {'8 AM to 9 AM': 'Medicine', '9:30 AM to 12 Noon': 'Postings', '2 PM to 3 PM': 'Pharmacology', '3 PM to 4 PM': 'Forensic Medicine CBL', '4 PM to 5 PM': 'Forensic Medicine Practicals'}, 2: {'8 AM to 9 AM': 'Community Medicine', '9:30 AM to 12 Noon': 'Postings', '2 PM to 3 PM': 'Pathology', '3 PM to 4 PM': 'Pathology practicals', '4 PM to 5 PM': 'nan'}, 3: {'8 AM to 9 AM': 'Pharmacology', '9:30 AM to 12 Noon': 'Postings', '2 PM to 3 PM': 'Microbiology', '3 PM to 4 PM': 'Pharmacology practicals', '4 PM to 5 PM': 'nan'}, 4: {'8 AM to 9 AM': 'Surgery', '9:30 AM to 12 Noon': 'Postings', '2 PM to 3 PM': 'Pathology', '3 PM to 4 PM': 'Community Medicine practicals', '4 PM to 5 PM': 'nan'}, 5: {'8 AM to 9 AM': 'Forensic Medicine/Microbiology', '9:30 AM to 12 Noon': 'Postings', '2 PM to 3 PM': 'Pharmacology', '3 PM to 4 PM': 'Bio Ethics*', '4 PM to 5 PM': 'nan'}},'batch_b':{0: {'8 AM to 9 AM': 'Microbiology', '9:30 AM to 12 Noon': 'Postings', '2 PM to 3 PM': 'Pathology', '3 PM to 4 PM': 'Pathology practicals', '4 PM to 5 PM': 'nan'}, 1: {'8 AM to 9 AM': 'Medicine', '9:30 AM to 12 Noon': 'Postings', '2 PM to 3 PM': 'Pharmacology', '3 PM to 4 PM': 'Microbiology practicals', '4 PM to 5 PM': 'nan'}, 2: {'8 AM to 9 AM': 'Community Medicine', '9:30 AM to 12 Noon': 'Postings', '2 PM to 3 PM': 'Pathology', '3 PM to 4 PM': 'Pharmacology practicals', '4 PM to 5 PM': 'nan'}, 3: {'8 AM to 9 AM': 'Pharmacology', '9:30 AM to 12 Noon': 'Postings', '2 PM to 3 PM': 'Microbiology', '3 PM to 4 PM': 'Forensic Medicine CBL', '4 PM to 5 PM': 'Forensic Medicine Practicals'}, 4: {'8 AM to 9 AM': 'Surgery', '9:30 AM to 12 Noon': 'Postings', '2 PM to 3 PM': 'Pathology', '3 PM to 4 PM': 'Community Medicine practicals', '4 PM to 5 PM': 'nan'}, 5: {'8 AM to 9 AM': 'Forensic Medicine/Microbiology', '9:30 AM to 12 Noon': 'Postings', '2 PM to 3 PM': 'Pharmacology', '3 PM to 4 PM': 'Bio Ethics*', '4 PM to 5 PM': 'nan'}}}
    classes = classes[batch]
    if get_day(date) == 6:
        return
    return classes[get_day(date)]
def get_day(date):
    d = dateutil.parser.parse(date)
    return int(d.weekday())
