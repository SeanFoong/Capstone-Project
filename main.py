from flask import Flask, render_template, request
from storage import Club, Activity, Membership, Participation
import validate
from data import StudentDB, ClassDB, SubjectDB, ClubDB

app = Flask('app')

ActivityDB = Activity()
MembershipDB = Membership()
ParticipationDB = Participation()

@app.route('/')
def splash():
    return render_template('splash.html')


@app.route('/add', methods=['GET', 'POST'])
def add():
    """Allow users to select a category of data and 
    add a record to the database under that category."""
    
    form_data = dict(request.form)
 
    if len(request.args) == 0:  # First page
        html = render_template(
            'add.html',
            page_type='add',
            form_meta={'action':'/add?new',
                       'method':'POST'},
        )
                                          
    elif 'new' in request.args:  #First input 
        # Checks type chosen and sets data fields
        if form_data['type'] == 'Club':
            form_data['Club Name'] = ''
        else:
            form_data['Activity Name'] = ''
            form_data['Start Date'] = ''
            form_data['End Date'] = ''
            form_data['Description'] = ''
        html = render_template(
            'add.html',      
            page_type='new',
            form_meta={'action':'/add?confirm',
                       'method':'POST'},
            form_data=form_data,
        )
                
    elif 'confirm' in request.args:  # Checking input for confirmation
        if form_data['type'] == 'Club':
            club_name = form_data['Club Name']
            
            if not validate.name(club_name): # Invalid club name
                html = render_template(
                    'add.html',      
                    page_type='new',
                    form_meta={'action':'/add?confirm',
                               'method':'POST'},
                    form_data=form_data,
                    invalid = ['Club Name']
                )
                return html

            # Club already exists
            if ClubDB.find(club_name) is not None:
                html = render_template(
                    'add.html',      
                    page_type='new',
                    form_meta={'action':'/add?confirm',
                               'method':'POST'},
                    form_data=form_data, 
                    present=f'{club_name} already exists.'
                )
                return html
                
        else:
            invalid = []
            activity_name = form_data['Activity Name']
            
            if not validate.name(activity_name):
                invalid.append('Activity Name')
            if not validate.date(form_data['Start Date']):
                invalid.append('Start Date')
            if not validate.date(form_data['End Date']):
                invalid.append('End Date')
            if not validate.description(form_data['Description']):
                invalid.append('Description')
                
            if invalid:  # Invalid activity data
                html = render_template(
                    'add.html',      
                    page_type='new',
                    form_meta={'action':'/add?confirm',
                               'method':'POST'},
                    form_data=form_data,
                    invalid=invalid
                )
                return html

            # Activity already exists
            if ActivityDB.find(activity_name) is not None: 
                html = render_template(
                    'add.html',      
                    page_type='new',
                    form_meta={'action':'/add?confirm',
                               'method':'POST'},
                    form_data=form_data,
                    present=f'{activity_name} already exists'
                )
                return html

            form_data['Description'] = form_data['Description'].capitalize()
                
        html = render_template(
            'add.html',
            page_type='confirm',
            form_meta={'action':'/add?success',
                       'method':'POST'},
            form_data=form_data
        )

    elif 'edit' in request.args:  #Editing input 
        html = render_template(
            'add.html',
            page_type='new',
            form_meta={'action':'/add?confirm',
                       'method':'POST'},
            form_data=form_data,
        )

    else:  # Insertion into database
        if form_data['type'] == 'Club':
            name = form_data['Club Name']
            record = {'name': name}
            ClubDB.insert(record) # Insert record into Club database
            
        else:
            name = form_data['Activity Name']
            record = {
                'name': name,
                'start_date': form_data['Start Date'], 
                'end_date': form_data['End Date'], 
                'description': form_data['Description'],
            }
            ActivityDB.insert(record) # Insert record into Activity database
            
        html = render_template(
            'add.html',
            page_type='success',
            name=name,
        )
    
    return html  # Renders page

    
@app.route('/view', methods=['GET', 'POST'])
def view():
    """Allow users to select a category of data and search for a 
    record within the database under that category."""

    form_data = dict(request.form)
    
    if len(request.args) == 0:   # First entry into /view
        html = render_template(
            'view.html',
            page_type='view',
            form_meta={'action':'/view?search',
                       'method':'POST'},
        )
        
    elif 'search' in request.args:      # After selection of category
        if form_data['type'] == 'Student':
            form_data['Student Name'] = ''
            all_values = StudentDB.findAll()            
            
        elif form_data['type'] == 'Class':
            form_data['Class Name'] = ''
            all_values = ClassDB.findAll()
            
        elif form_data['type'] == 'Club':
            form_data['Club Name'] = ''
            all_values = ClubDB.findAll()
            
        else:
            form_data['Activity Name'] = ''
            all_values = ActivityDB.findAll()
            
        html = render_template(
            'view.html',
            page_type='search',
            form_meta={'action':'/view?result',
                       'method':'POST'},
            form_data=form_data,
            all_values=all_values
        )

    elif 'result' in request.args:        # After input of data to be searched
        if form_data['type'] == 'Student':  # Searching Student
            form_data['Student Name'] = form_data['Student Name'].upper()
            student_name = form_data['Student Name']
            
            if validate.name(student_name):   # Validation
                data = StudentDB.find(student_name)

                if data is not None:  # Record present
                    form_data['Age'] = data['age']
                    form_data['Year Enrolled'] = data['year_enrolled']
                    form_data['Graduating Year'] = data['graduating_year']
                    form_data['Class'] = data['class']
                    
                else:   # Record not present
                    html = render_template(
                        'view.html', 
                        page_type='search',
                        form_meta={'action':'/view?result',
                                   'method':'POST'},
                        form_data=form_data,
                        invalid='Student Name Not Found',
                        all_values=StudentDB.findAll()
                    )
                    return html
                
            else:  # Validation failure
                html = render_template(
                    'view.html',
                    page_type='search',
                    form_meta={'action':'/view?result',
                               'method':'POST'},
                    form_data=form_data,
                    invalid='Student Name Invalid',
                    all_values=StudentDB.findAll()
                )
                return html
                
        elif form_data['type'] == 'Class':  # Searching Class
            class_name = form_data['Class Name']
            
            if validate.class_name(class_name):   # Validation
                data = ClassDB.find(class_name)

                if data is not None:   # Record present
                    form_data['Level'] = data['level']
                    
                else:    # Record not present
                    html = render_template(
                        'view.html', 
                        page_type='search',
                        form_meta={'action':'/view?result',
                                   'method':'POST'},
                        form_data=form_data,
                        invalid='Class Name Not Found',
                        all_values=ClassDB.findAll()
                    )
                    return html
                
            else:   # Validation failure
                html = render_template(
                    'view.html', 
                    page_type='search',
                    form_meta={'action':'/view?result',
                               'method':'POST'},
                    form_data=form_data,
                    invalid='Class Name Invalid',
                    all_values=ClassDB.findAll()
                )
                return html
                
        elif form_data['type'] == 'Club':  # Searching Club
            club_name = form_data['Club Name']
            
            if validate.name(club_name):  # Validation
                data = ClubDB.find(club_name)

                if data is not None:  # Record present
                    form_data['ID'] = data['id']
                    
                else:  # Record not present
                    html = render_template(
                        'view.html', 
                        page_type='search',
                        form_meta={'action':'/view?result',
                                   'method':'POST'},
                        form_data=form_data,
                        invalid='Club Name Not Found',
                        all_values=ClubDB.findAll()
                    )
                    return html
                
            else:  # Validation failure
                html = render_template(
                    'view.html', 
                    page_type='search',
                    form_meta={'action':'/view?result',
                               'method':'POST'},
                    form_data=form_data,
                    invalid='Club Name Invalid',
                    all_values=ClubDB.findAll()
                )
                return html
              
        else:  # Searching Activity
            activity_name = form_data['Activity Name']
            
            if validate.name(activity_name):  # Validation
                data = ActivityDB.find(activity_name)

                if data is not None:  # Record present
                    form_data['Start Date'] = data['start_date']
                    form_data['End Date'] = data['end_date']
                    form_data['Description'] = data['description']
                    
                else:  # Record not present
                    html = render_template(
                        'view.html', 
                        page_type='search',
                        form_meta={'action':'/view?result',
                                   'method':'POST'},
                        form_data=form_data,
                        invalid='Activity Name Not Found',
                        all_values=ActivityDB.findAll()
                    )
                    return html
                
            else:  # Validation failure
                html = render_template(
                    'view.html', 
                    page_type='search',
                    form_meta={'action':'/view?result',
                               'method':'POST'},
                    form_data=form_data,
                    invalid='Activity Name Invalid',
                    all_values=ActivityDB.findAll()
                )
                return html

        html = render_template(
            'view.html',
            page_type='result',
            form_data=form_data,
        )

    return html


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    """Allow users to select a category of data and search for a record 
    within the database under that category, then edit that record."""
    form_data = dict(request.form)

    if len(request.args) == 0:  # First entry into /edit
        html = render_template(
            'edit.html',
            page_type='edit',
            form_meta={'action':'/edit?search','method':'POST'},
        )

    elif 'search' in request.args:  # After selection of category
        form_data['Student Name'] = ''
        form_data['Club Name'] = ''
        
        if form_data['type'] == 'Participation':
            form_data['Activity Name'] = ''
        
        html = render_template(
            'edit.html',
            page_type='search',
            form_meta={'action':'/edit?result','method':'POST'},
            form_data=form_data,
        )
    
    elif 'result' in request.args:  # Search database
        form_data['Student Name'] = form_data['Student Name'].upper()
        student_name = form_data['Student Name']
        club_name = form_data['Club Name']
        invalid = []
        
        if not validate.name(student_name):   # Validation for names
            invalid.append('Student Name')
        if not validate.name(club_name):   # Validation failure
            invalid.append('Club Name')

        # Validate for activity name in participation 
        if form_data['type'] == 'Participation':
            activity_name = form_data['Activity Name']
            if not validate.name(activity_name):
                invalid.append('Activity Name')

        if invalid:   # Validation failure
            html = render_template(
                'edit.html',      
                page_type='search',
                form_meta={'action':'/edit?result',
                           'method':'POST'},
                form_data=form_data,
                invalid=invalid
            )
            return html
        
        student_id = StudentDB.findID(student_name)
        club_id = ClubDB.findID(club_name)

        absent = []  
        if student_id is None:  # Check if student exists in db
            absent.append('Student Name')

        if club_id is None:   # Check if class id exists in db
            absent.append('Club Name')

        # Validate for activity name in participation
        if form_data['type'] == 'Participation':
            activity_id = ActivityDB.findID(activity_name)
            if activity_id is None:
                absent.append('Activity Name')

        if absent:
            html = render_template(
                'edit.html',      
                page_type='search',
                form_meta={'action':'/edit?result',
                           'method':'POST'},
                form_data=form_data,
                absent=absent
            )
            return html

        membership_data = MembershipDB.find(student_id, club_id)
                
        if form_data['type'] == 'Membership':            
            if membership_data is not None:  # Checks if membership in db                
                form_data['Role'] = membership_data['role']

                html = render_template(
                    'edit.html',
                    page_type='result',
                    form_meta={'action':'edit?confirm',
                               'method':'POST'},
                    form_data=form_data,
                )

            else:  # If membership not in db
                html = render_template(
                    'edit.html',
                    page_type='add',
                    form_meta={'action':'edit?add_new',
                               'method':'POST'},
                    form_data=form_data,
                    partic_not_member=False
                )
                
        else:            
            participation_data = ParticipationDB.find(student_id, club_id, activity_id)

            if participation_data is not None:  # Checks if the participation exists in db
                form_data['Category'] = participation_data['category']
                form_data['Role'] = participation_data['role']
                form_data['Award'] = participation_data['award']
                form_data['Hours'] = participation_data['hours']
        
                html = render_template(
                    'edit.html',
                    page_type='result',
                    form_meta={'action':'edit?confirm',
                               'method':'POST'},
                    form_data=form_data,
                )  
 
            # If membership not in db
            elif membership_data is None:
                form_data['type'] = 'Membership'
                del form_data['Activity Name']
                
                html = render_template(
                    'edit.html',
                    page_type='add',
                    form_meta={'action':'edit?add_new',
                               'method':'POST'},
                    form_data=form_data,
                    partic_not_member=True
                )

            # Checks if membership in db but student not in activity
            else:
                html = render_template(
                    'edit.html',
                    page_type='add',
                    form_meta={'action':'edit?add_new',
                               'method':'POST'},
                    form_data=form_data,
                    partic_not_member=False
                )

    elif 'confirm' in request.args:
        student_name = form_data['Student Name']
        club_name = form_data['Club Name']
        student_id = StudentDB.findID(student_name)        
        club_id = ClubDB.findID(club_name)
        invalid = []
        
        if form_data['type'] == 'Membership':
            membership_data = MembershipDB.find(student_id, club_id)
            
            # Invalid membership data
            if not validate.membership_role(form_data['Role']):
                invalid.append('Role')
                form_data['Role'] = membership_data['role']
                html = render_template(
                    'edit.html',
                    page_type='result',
                    form_meta={'action':'/edit?confirm',
                               'method':'POST'},
                    form_data=form_data,
                    invalid=invalid
                )
                return html
                
        else:            
            # Validation for data in participation
            if not validate.category(form_data['Category']):
                invalid.append('Category')
            if not validate.participation_role(form_data['Role']):
                invalid.append('Role')
            if not validate.name(form_data['Award']):
                invalid.append('Award')
            if not validate.hours(form_data['Hours']):
                invalid.append('Hours')
                
            if invalid:  # Invalid participation data
                activity_name = form_data['Activity Name']
                activity_id = ActivityDB.findID(activity_name)
                participation_data = ParticipationDB.find(student_id, club_id, activity_id)
                form_data['Category'] = participation_data['category']
                form_data['Role'] = participation_data['role']
                form_data['Award'] = participation_data['award']
                form_data['Hours'] = participation_data['hours']
                
                html = render_template(
                    'edit.html',      
                    page_type='result',
                    form_meta={'action':'/edit?confirm',
                               'method':'POST'},
                    form_data=form_data,
                    invalid=invalid
                )
                return html

        particulars = {'Student Name':student_name,
                       'Club Name':club_name}
        old_data = {}

        if form_data['type'] == 'Membership':
            curr_data = MembershipDB.find(student_id, club_id)
        else:
            activity_name = form_data['Activity Name']
            activity_id = ActivityDB.findID(activity_name)
            curr_data = ParticipationDB.find(student_id, club_id, activity_id)
            particulars['Activity Name'] = activity_name

        for key, value in curr_data.items():
            key = key.title()
            old_data[key] = value

        html = render_template(
            'edit.html',
            page_type='confirm',
            form_meta={'action':'edit?success',
                       'method':'POST'},
            form_data=form_data,
            old_data=old_data,
            particulars=particulars
        )
        
    elif 'success' in request.args:  # Success page 
        role = form_data['Role']
        student_name = form_data['Student Name']
        club_name = form_data['Club Name']
        student_id = StudentDB.findID(student_name)
        club_id = ClubDB.findID(club_name)
        
        if form_data['type'] == 'Membership':
            MembershipDB.update(role, student_id, club_id)
            
        else:
            activity_name = form_data['Activity Name']
            activity_id = ActivityDB.findID(activity_name)
            category = form_data['Category']
            award = form_data['Award']
            hours = int(form_data['Hours'])
            ParticipationDB.update(category, role, award, hours, 
                                   student_id, club_id, activity_id) 
        
        name = list(form_data.values())[1]
        
        html = render_template(
            'edit.html',
            page_type='success',
            name=name,
            type=form_data['type'],
        )

    elif 'add_new' in request.args:
        # Checks type chosen and sets data fields
        if form_data['type'] == 'Membership':
            form_data['Role'] = ''
        else:
            form_data['Category'] = ''
            form_data['Role'] = ''
            form_data['Award'] = ''
            form_data['Hours'] = ''

        html = render_template(
            'edit.html',      
            page_type='add_new',
            form_meta={'action':'/edit?add_confirm',
                       'method':'POST'},
            form_data=form_data,
        )

    elif 'add_confirm' in request.args:
        if form_data['type'] == 'Membership':
            role = form_data['Role']
            
            if not validate.membership_role(role): # Invalid club name
                html = render_template(
                    'edit.html',      
                    page_type='add_new',
                    form_meta={'action':'/edit?add_confirm',
                               'method':'POST'},
                    form_data=form_data,
                    invalid = ['Role']
                )
                return html
                
        else:
            invalid = []
            
            if not validate.category(form_data['Category']):
                invalid.append('Category')
            if not validate.participation_role(form_data['Role']):
                invalid.append('Role')
            if not validate.name(form_data['Award']):
                invalid.append('Award')
            if not validate.hours(form_data['Hours']):
                invalid.append('Hours')

            if invalid:  # Invalid activity data
                html = render_template(
                    'edit.html',      
                    page_type='add_new',
                    form_meta={'action':'/edit?add_confirm',
                               'method':'POST'},
                    form_data=form_data,
                    invalid=invalid
                )
                return html

        html = render_template(
            'edit.html',
            page_type='add_confirm',
            form_meta={'action':'/edit?add_success',
                       'method':'POST'},
            form_data=form_data
        )

    elif 'add_edit' in request.args:
        html = render_template(
            'edit.html',
            page_type='add_new',
            form_meta={'action':'/edit?add_confirm',
                       'method':'POST'},
            form_data=form_data,
        )

    else:
        record = {}
        student_name = form_data['Student Name']
        club_name = form_data['Club Name']

        student_id = StudentDB.findID(student_name)
        club_id = ClubDB.findID(club_name)
        role = form_data['Role']
        
        if form_data['type'] == 'Membership':            
            record = {
                'student_id': student_id,
                'club_id': club_id,
                'role': role
            }            
            MembershipDB.insert(record) # Insert record into Club database

            entity_name = club_name
            
        else:
            activity_name = form_data['Activity Name']
            activity_id = ActivityDB.findID(activity_name)
            category = form_data['Category']
            award = form_data['Award']
            hours = int(form_data['Hours'])
            
            name = form_data['Activity Name']
            record = {
                'student_id': student_id,
                'club_id': club_id, 
                'activity_id': activity_id, 
                'category': category,
                'role': role,
                'award': award,
                'hours': hours,
            }
            ParticipationDB.insert(record) # Insert record into Activity database

            entity_name = activity_name
            
        html = render_template(
            'edit.html',
            page_type='add_success',
            student_name=student_name,
            entity_name=entity_name,
            type=form_data['type']
        )

    return html


app.run(host='0.0.0.0', port=8080)