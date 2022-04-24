from flask import Flask, render_template, request
from storage import Club, Activity, StudentClub, StudentActivity
from convert import convert
import validate
from data import StudentDB, ClassDB, SubjectDB, ClubDB

app = Flask('app')

ActivityDB = Activity()
StudentClubDB = StudentClub()
StudentActivityDB = StudentActivity()


@app.route('/')
def splash():
    return render_template('splash.html')


@app.route('/add', methods=['GET', 'POST'])
def add():
    """Allow users to select a category of data and 
    add a record to the database under that category."""
    
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
        if form_data['type'] == 'Club':
            if validate.name(form_data['Club Name']):
                pass
            else:
                form_data['Club Name'] = 'Invalid'
                html = render_template('add.html',      
                               page_type='new',
                               form_meta={'action':'/add?edit',
                                          'method':'POST'},
                               form_data=form_data)
                return html
        else:
            error = False
            
            if not validate.name(form_data['Activity Name']):
                form_data['Activity Name'] = 'Invalid'
                error = True
            if not validate.date(form_data['Start Date']):
                form_data['Start Date'] = 'Invalid'
                error = True
            if not validate.date(form_data['End Date']):
                form_data['End Date'] = 'Invalid'
                error = True
            if not validate.description(form_data['Description']):
                form_data['Description'] = 'Invalid'
                error = True
            if not validate.name(form_data['Club']):
                form_data['Club'] = 'Invalid'
                error = True
            if not validate.category(form_data['Category']):
                form_data['Category'] = 'Invalid'
                error = True
                
            if error:
                html = render_template('add.html',      
                               page_type='new',
                               form_meta={'action':'/add?edit',
                                          'method':'POST'},
                               form_data=form_data)
                return html
                
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
            ClubDB.insert(record) # Insert record into Club database
            
        else:
            name = form_data['Activity Name']
            record = {'name': name,
                      'start_date': form_data['Start Date'], 
                      'end_date': form_data['End Date'], 
                      'description': form_data['Description']
                     }
            ActivityDB.insert(record) # Insert record into Activity database
            
        html = render_template('add.html',
                               page_type='success',
                               name=name)
    
    return html  # Renders page

    
@app.route('/view', methods=['GET', 'POST'])
def view():
    """Allow users to select a category of data and search for a 
    record within the database under that category."""

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
        if form_data['type'] == 'Student':
            student_name = form_data['Student Name']
            data = StudentDB.find(student_name)

            if validate.name(form_data['Student Name']):
                student_name = form_data['Student Name']
                data = StudentDB.find(student_name)
                
                if data is not None:  # Record present
                    form_data['Age'] = data[2]
                    form_data['Year enrolled'] = data[3]
                    form_data['Graduating year'] = data[4]
                    form_data['Class'] = data[5]
                    
                else: 
                    html = render_template('view.html', 
                                           page_type='error',
                                           form_data=form_data)
                    return html
                
            else:  # Invalid
                html = render_template('view.html', 
                                       page_type='error',
                                       form_data=form_data)
                return html
                
        elif form_data['type'] == 'Class':
            if validate.class_name(form_data['Class Name']):
                class_name = int(form_data['Class Name'])
                data = ClassDB.find(class_name)

                if data is not None:
                    form_data['Level'] = data[2]
                else: 
                    html = render_template('view.html', 
                                           page_type='error',
                                           form_data=form_data)
                    return html
                
            else:
                html = render_template('view.html', 
                                       page_type='error',
                                       form_data=form_data)
                return html
                
        elif form_data['type'] == 'Club':
            if validate.name(form_data['Club Name']):
                club_name = form_data['Club Name']
                data = ClubDB.find(club_name)

                if data is not None:
                    form_data['id'] = data[0]
                    
                else: 
                    html = render_template('view.html', 
                                           page_type='error',
                                           form_data=form_data)
                    return html
                
            else:
                html = render_template('view.html', 
                                       page_type='error',
                                       form_data=form_data)
                return html
              
        else:
            if validate.name(form_data['Activity Name']):
                activity_name = form_data['Activity Name']
                data = ActivityDB.find(activity_name)
                
                if data is not None:
                    activity_name = form_data['Activity Name']
                    data = ActivityDB.find(activity_name)
                    form_data['Start Date'] = data[2]
                    form_data['End Date'] = data[3]
                    form_data['Description'] = data[4]
                    
                else: 
                    html = render_template('view.html', 
                                           page_type='error',
                                           form_data=form_data)
                    return html
                
            else:
                html = render_template('view.html', 
                                       page_type='error',
                                       form_data=form_data)
                return html

        html = render_template('view.html',
                               page_type='result',
                               form_data=form_data)

    return html


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    """Allow users to select a category of data and search for a record 
    within the database under that category, then edit that record."""
    form_data = dict(request.form)

    if len(request.args) == 0:
        html = render_template('edit.html',
                               page_type='edit',
                               form_meta={'action':'/edit?search',
                                          'method':'POST'})

    elif 'search' in request.args:
        form_data['Student Name'] = ''
        
        if form_data['type'] == 'Membership':
            form_data['Club Name'] = ''
        else:
            form_data['Activity Name'] = ''
        
        html = render_template('edit.html',
                               page_type='search',
                               form_meta={'action':'/edit?result',
                                          'method':'POST'},
                               form_data=form_data)
        
    elif 'result' in request.args:
        # Search database
        student_name = form_data['Student Name']
        club_name = ''
        activity_name = ''
        student_id = StudentDB.findID(student_name)
        
        if student_id is not None: # Check if student exists in db
            if form_data['type'] == 'Membership':
                club_name = form_data['Club Name']
                club_id = ClubDB.findID(club_name)

                if club_id is not None:  # Checks if the club exists in db
                    membership_data = StudentClubDB.find(student_id, club_id)
                    print(student_id, club_id)
                    print(membership_data) 
                    
                    if membership_data is not None: # Checks if student in club
                        print(membership_data)
                        form_data['Role'] = ''

                        html = render_template('edit.html',
                                               page_type='result',
                                               form_meta={'action':'edit?confirm',
                                                          'method':'POST'},
                                               form_data=form_data)
                        return html

            
            elif form_data['type'] == 'Participation':
                activity_name = form_data['Activity Name']
                activity_id = ActivityDB.findID(activity_name)
                
                if activity_id is not None: # Checks if the activity exists in db
                    participation_data = StudentActivityDB.find(student_id, activity_id)
                    
                    if participation_data is not None: # Checks if student is participant
                        form_data['Category'] = ''
                        form_data['Role'] = ''
                        form_data['Award'] = ''
                        form_data['Hours'] = ''
                
                        html = render_template('edit.html',
                                               page_type='result',
                                               form_meta={'action':'edit?confirm',
                                                          'method':'POST'},
                                               form_data=form_data)
                        return html

        html = render_template('edit.html',
                               page_type='error',
                               form_data=form_data)
        return html

    elif 'confirm' in request.args:
        print('confirm', form_data)
        student_name = form_data['Student Name']
        student_id = StudentDB.findID(student_name)
        old_data = {}

        if form_data['type'] == 'Membership':
            club_name = form_data['Club Name']
            club_id = ClubDB.findID(club_name)
            curr_data = StudentClubDB.find(student_id, club_id)
        else:
            activity_name = form_data['Activity Name']
            activity_id = ActivityDB.findID(activity_name)
            curr_data = StudentActivityDB.find(student_id, activity_id)

        counter = 0
        for key in form_data.keys():
            if key != 'type':
                if key =='Student Name':
                    old_data[key] = student_name
                elif key == 'Club Name':
                    old_data[key] = club_name
                elif key == 'Activity Name':
                    old_data[key] = activity_name
                else:
                    old_data[key] = curr_data[counter]
                counter += 1

        html = render_template('edit.html',
                               page_type='confirm',
                               form_meta={'action':'edit?success',
                                          'method':'POST'},
                               form_data=form_data,
                               old_data = old_data)
        
    else:
        role = form_data['Role']
        student_name = form_data['Student Name']
        student_id = StudentDB.findID(student_name)
        
        if form_data['type'] == 'Membership':
            club_name = form_data['Club Name']
            club_id = ClubDB.findID(club_name)
            StudentClubDB.update(club_id, role, student_id)
        else:
            activity_name = form_data['Activity Name']
            category = form_data['Category']
            award = form_data['Award']
            hours = form_data['Hours']
            activity_id = ActivityDB.findID(activity_name)
            StudentActivityDB.update(activity_id, category, role, award, hours, student_id) 

        name = list(form_data.values())[1]
        html = render_template('edit.html',
                               page_type='success',
                               name=name)    

    return html


app.run(host='0.0.0.0', port=8080)