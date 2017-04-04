from flask import request,redirect, Flask, render_template,jsonify
import dateutil.parser
from timetable import get_schedule
app = Flask(__name__)
@app.route('/',methods = ['GET'])
def index():
    return render_template('landing.html')
@app.route('/classdata',methods = ['GET'])
def class_data():
    """Request class data with params date=(2017-12-31) and batch=batch_a"""
    date = request.args.get('date')
    print(date)
    batch = request.args.get('batch')
    print(batch)
    return jsonify(get_schedule(date,batch))
