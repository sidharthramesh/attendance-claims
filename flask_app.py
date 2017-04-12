from flask import request, Flask, render_template,jsonify
from flask_sqlalchemy import SQLAlchemy
import dateutil.parser
from config import SQLALCHEMY_DATABASE_URI
from flask_migrate import Migrate
app = Flask(__name__,static_url_path='/static')
app.config["DEBUG"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
db = SQLAlchemy(app)
migrate = Migrate(app, db)
from models import *
def get_schedule(date,batch):
    day = dateutil.parser.parse(date).weekday()+1
    return Period.query.filter_by(day=day, batch = Batch.query.filter_by(name=batch).first()).order_by(Period.start_time).all()

@app.route('/',methods = ['GET','POST'])
def index():
    batches = [{'name':batch.name,'id':batch.id} for batch in Batch.query.order_by(Batch.name)]
    if request.method == 'POST':
        date = request.form.get('date')
        print(batches)
        return render_template('index.html',heading = 'Hello there!', form=request.form, classes = get_schedule(date), batches = batches)
    else:
        return render_template('index.html',heading = 'Hello there!',form=None,batches = batches)
@app.route('/classdata',methods = ['GET'])
def class_data():
    """Request class data with params date=(2017-12-31) and batch=batch_a"""
    if request.method == 'GET':
        date = request.args.get('date')
        batch = request.args.get('batch')
        if date and batch:
            classes = []
            for period in get_schedule(date,batch):
                class_obj = {'id':period.id, 'name' : period.name, 'start_time':str(period.start_time), 'end_time':str(period.end_time),'ask_dept':True}
                if not period.department_id == None:
                    class_obj['ask_dept'] = False
                classes.append(class_obj)
            return jsonify(classes)

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return "Not found page", 404
