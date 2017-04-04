from flask import request,redirect, Flask, render_template
import dateutil.parser
from timetable import get_schedule
app = Flask(__name__)
@app.route('/',methods = ['GET'])
def index(variable):
    return "Work in progress..."
@app.route('/classdata',methods = ['GET'])
def class_data():
    date = request.args.get('date')
    print(date)
    batch = request.args.get('batch')
    print(batch)
    return get_schedule(date,batch)

if __name__ == '__main__':
    app.run()
