from flask_app import db
for i in reversed(db.metadata.sorted_tables):
    print("Deleting {}".format(i))
    db.session.execute(i.delete())
    db.session.commit()
