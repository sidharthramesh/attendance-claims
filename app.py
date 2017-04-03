from flask import request,redirect, Flask, render_template

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('form.html')
@app.route('/submit',methods = ['POST'])
def form_handle():
    print('Got form!')
    name = request.form['name']
    date = request.form['date']
    print('The name is {}\nDate is {}'.format(name,date))
    print(type(date))
    return render_template('thankyou.html',name = name)

if __name__ == '__main__':
    app.run()
