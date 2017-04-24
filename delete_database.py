
from flask_app import db
for i in reversed(db.metadata.sorted_tables):
    if input("Delete {} Y/n?".format(i)).lower() in ['y','yes']:
        print("Deleting {}".format(i))
        db.session.execute(i.delete())
        db.session.commit()
    
