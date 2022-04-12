from flask import Flask, render_template, request
app = Flask('app')

@app.route('/')
def splash():
  return render_template('splash.html')

@app.route('/add', methods=['GET'])
def add():
    if page_type == 


    else:
        html = render_template('form_student.html',
                               page_type='new_club',
                               form_meta={'action':'/add?new_club',
                                          'method':'POST'},
                               form_data={'club_name':'',
                                          'clubclub':''})
    return html

@app.route('/view', methods=['GET'])
def view():
    return render_template('view.html')

@app.route('/edit', methods=['GET'])
def edit():
    return render_template('edit.html')
    
app.run(host='0.0.0.0', port=8080)