from flask import Flask, render_template, request
from storage import Club, Activity
from convert import convert
import validate
from data import StudentDB, ClassDB, SubjectDB

app = Flask('app')

ClubDB = Club()
ActivityDB = Activity()

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
        record = {}
        
        if form_data['type'] == 'Club':
            name = form_data['Club Name']
            record = {'name': name}
            ClubDB.insert(record) # insert record into Club database
            
        elif form_data['type'] == 'Activity':
            name = form_data['Activity Name']
            record = {'name': name,
                      'start_date': form_data['Start Date'], 
                      'end_date': form_data['End Date'], 
                      'description': form_data['Description']
                     }
            ActivityDB.insert(record) # insert record into Activity database
            
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
        if form_data['type'] == 'Student':
            student_name = form_data['Student Name']
            data = StudentDB.find(student_name)
            form_data['Age'] = data[2]
            form_data['Year enrolled'] = data[3]
            form_data['Graduating year'] = data[4]
            form_data['Class'] = data[5]

        elif form_data['type'] == 'Class':
            class_name = form_data['Class Name']
            data = ClassDB.find(class_name)
            print(data)
            form_data['Level'] = data[2]

        elif form_data['type'] == 'Club':
            club_name = form_data['Club Name']
            data = ClubDB.find(club_name)
            form_data['id'] = data[0]
            
        elif form_data['type'] == 'Activity':
            activity_name = form_data['Activity Name']
            data = ActivityDB.find(activity_name)
            form_data['Start Date'] = data[2]
            form_data['End Date'] = data[3]
            form_data['Description'] = data[4]
            
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

