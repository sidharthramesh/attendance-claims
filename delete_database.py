from flask_app import db
for i in reversed(db.metadata.sorted_tables):
    db.session.execute(i.delete())
    db.session.commit()
