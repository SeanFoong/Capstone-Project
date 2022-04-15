from flask import Flask, render_template, request
app = Flask('app')


@app.route('/')
def splash():
  return render_template('splash.html')


@app.route('/add', methods=['GET', 'POST'])
def add():
    form_data = dict(request.form)
 
    if len(request.args) == 0:
        html = render_template('add.html',
                               page_type='add')
        
    elif 'new' in request.args:
        if form_data['type'] == 'Club':
            form_data['Club Name'] = ''
        else:
            form_data['Activity Name'] = ''
            form_data['Start Date'] = ''
            form_data['End Date'] = ''
            form_data['Description'] = ''           

        html = render_template('add.html',
                               page_type='new',
                               form_meta={'action':'/add?confirm',
                                          'method':'POST'},
                               form_data=form_data)
            
    elif 'confirm' in request.args:
        html = render_template('add.html',
                               page_type='confirm',
                               form_meta={'action':'/add?success',
                                          'method':'POST'},
                               form_data=form_data)

    elif 'edit' in request.args:
        html = render_template('add.html',
                               page_type='new',
                               form_meta={'action':'/add?confirm',
                                          'method':'POST'},
                               form_data=form_data)

    else:
        name = list(form_data.values())[1]
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