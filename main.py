from flask import Flask, render_template, request
app = Flask('app')


@app.route('/')
def splash():
  return render_template('splash.html')


@app.route('/add', methods=['GET', 'POST'])
def add():
    """Allow users to select a category of data and add a record to the database under that category."""
    form_data = dict(request.form)
 
    if len(request.args) == 0:  # First page
        html = render_template('add.html',
                               page_type='add',
                               form_meta={'action':'/add?new',
                                          'method':'POST'})
        
    elif 'new' in request.args:
        # Checks type chosen and sets data fields
        if form_data['type'] == 'Club':
            form_data['Club Name'] = ''
        else:
            form_data['Activity Name'] = ''
            form_data['Start Date'] = ''
            form_data['End Date'] = ''
            form_data['Description'] = ''
            form_data['Club'] = ''
            form_data['Category'] = ''

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
        # add data to the database here
        name = list(form_data.values())[1]
        html = render_template('add.html',
                               page_type='success',
                               name=name)
    return html  # Renders page

    
@app.route('/view', methods=['GET', 'POST'])
def view():
    """Allow users to select a category of data and search for a record within the database under that category."""
    form_data = dict(request.form)
    
    if len(request.args) == 0:
        html = render_template('view.html',
                               page_type='view',
                               form_meta={'action':'/view?search',
                                          'method':'POST'})
        
    elif 'search' in request.args:
        if form_data['type'] == 'Student':
            form_data['Student Name'] = ''
        elif form_data['type'] == 'Class':
            form_data['Class Name'] = ''
        elif form_data['type'] == 'Club':
            form_data['Club Name'] = ''
        else:
            form_data['Activity Name'] = ''
        
        html = render_template('view.html',
                               page_type='search',
                               form_meta={'action':'/view?result',
                                          'method':'POST'},
                               form_data=form_data)

    elif 'result' in request.args:
        # search database here
        form_data['test'] = 'test'
        form_data['test1'] = 'test1'
        
        html = render_template('view.html',
                               page_type='result',
                               form_data=form_data)

    return html


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    """Allow users to select a category of data and search for a record within the database under that category, then edit that record."""
    form_data = dict(request.form)

    if len(request.args) == 0:
        html = render_template('edit.html',
                               page_type='edit',
                               form_meta={'action':'/edit?search',
                                          'method':'POST'})

    elif 'search' in request.args:
        if form_data['type'] == 'Membership':
            form_data['Membership Name'] = ''
        else:
            form_data['Participation Name'] = ''
        
        html = render_template('edit.html',
                               page_type='search',
                               form_meta={'action':'/edit?result',
                                          'method':'POST'},
                               form_data=form_data)
        
    elif 'result' in request.args:
        # search db
        # form_data[keys] = values
        
        html = render_template('edit.html',
                               page_type='result',
                               form_meta={'action':'edit?confirm',
                                          'method':'POST'},
                               form_data=form_data)

    elif 'confirm' in request.args:
        html = render_template('edit.html',
                               page_type='confirm',
                               form_meta={'action':'edit?success',
                                          'method':'POST'},
                               form_data=form_data)
        
    else:
        name = list(form_data.values())[1]
        html = render_template('edit.html',
                               page_type='success',
                               name=name)    
        
    return html
    
app.run(host='0.0.0.0', port=8080)