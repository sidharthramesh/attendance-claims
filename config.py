import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI_ = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_POOL_RECYCLE = 299

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="tornadoalert",
    password="databasepassword123",
    hostname="tornadoalert.mysql.pythonanywhere-services.com",
    databasename="tornadoalert$claims",
)
