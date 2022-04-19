from flask import Flask, render_template, request
from convert import convert
import validate


app = Flask('app')


@app.route('/')
def splash():
  return render_template('splash.html')


@app.route('/add', methods=['GET', 'POST'])
def add():
    form_data = dict(request.form)
    print(list(request.args))
    
    if len(request.args) == 0:
        html = render_template('add.html',
                               page_type='add')
        
    elif 'club' in request.args:
            html = render_template('add.html',
                                   page_type='add_club',
                                   form_meta={'action':'/add?confirm_club',
                                              'method':'POST'},
                                   form_data={'Club Name':''})
            
    elif 'confirm_club' in request.args:
        html = render_template('add.html',
                               page_type='confirm_club',
                               form_meta={'action':'/add?success',
                                          'method':'POST'},
                               form_data=form_data)

    elif 'edit_club' in request.args:
        html = render_template('add.html',
                               page_type='add_club',
                               form_meta={'action':'/add?confirm_club',
                                          'method':'POST'},
                               form_data=form_data)

    elif 'activity' in request.args:
            html = render_template('add.html',
                                   page_type='add_activity',
                                   form_meta={'action':'/add?confirm_activity',
                                              'method':'POST'},
                                   form_data={'Activity Name':'',
                                              'Start Date':'',
                                              'End Date':'',
                                              'Description':''})
                                   
    elif 'confirm_activity' in request.args:
        html = render_template('add.html',
                               page_type='confirm_activity',
                               form_meta={'action':'/add?success',
                                          'method':'POST'},
                               form_data=form_data)

    elif 'edit_activity' in request.args:
        html = render_template('add.html',
                               page_type='add_activity',
                               form_meta={'action':'/add?confirm_activity',
                                          'method':'POST'},
                               form_data=form_data)

    else:
        name = list(form_data.values())[0]
        html = render_template('add.html',
                               page_type='success',
                               name=name)
    return html

    
@app.route('/view', methods=['GET', 'POST'])
def view():
    return render_template('view.html')


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    return render_template('edit.html')
    
app.run(host='0.0.0.0', port=8080)