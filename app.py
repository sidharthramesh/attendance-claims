from flask import request,redirect, Flask, render_template

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('form.html')
@app.route('/submit',methods = ['POST'])
def form_handle():
    print('Got form!')
    return render_template('classes.html',form = request.form, classes = class_details(request.form))
@app.route('/submit_classes', methods = ['POST'])
def submit_classes():
    return render_template('thankyou.html')
def class_details(form):
    date = form['date']
    #mockup
    classes = [{'value':'pathology_p','name':'Pathology Practicals'},{'value':'microbio_t','name':'Microbiology Theory'}]
    return classes


if __name__ == '__main__':
    app.run()
