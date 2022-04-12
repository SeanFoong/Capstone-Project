from flask import Flask, render_template, request
app = Flask('app')

@app.route('/')
def splash():
  return render_template('splash.html')

@app_route('/add', methods=['POST'])
def add_club():
    form_data = dict(request.form)

app.run(host='0.0.0.0', port=8080)