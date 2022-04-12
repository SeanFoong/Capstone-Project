from flask import Flask
app = Flask('app')

@app.route('/')
def hello_world():
  return render_template('splash.html')

@app.route('/new_student', )
def new_student():
  if confirm in request.args()

  else:
    return render_template('')

@app.route('/')

app.run(host='0.0.0.0', port=8080)