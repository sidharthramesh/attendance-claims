import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_POOL_RECYCLE = 299

SQLALCHEMY_DATABASE_URI_ = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="tornadoalert",
    password="Supernova-7",
    hostname="tornadoalert.mysql.pythonanywhere-services.com",
    databasename="tornadoalert$claims",
)
