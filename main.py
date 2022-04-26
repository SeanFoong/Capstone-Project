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
            form_meta={'action':'/add?new', 'method':'POST'},
        )
                                          
        
    elif 'new' in request.args:    #First input 
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
            form_meta={'action':'/add?confirm', 'method':'POST'},
            form_data=form_data,
        )
                
    elif 'confirm' in request.args:    #Checking input for confirmation
        if form_data['type'] == 'Club':
            if validate.name(form_data['Club Name']):
                form_data['Club Name'] = form_data['Club Name'].title()
                
            else:
                html = render_template(
                    'add.html',      
                    page_type='new',
                    form_meta={'action':'/add?edit', 'method':'POST'},
                    form_data=form_data,
                    invalid = ['Student Name']
                )
                return html
                
        else:
            invalid = []
            
            if not validate.name(form_data['Activity Name']):
                invalid.append('Activity Name')
            if not validate.date(form_data['Start Date']):
                invalid.append('Start Date')
            if not validate.date(form_data['End Date']):
                invalid.append('End Date')
            if not validate.description(form_data['Description']):
                invalid.append('Description Name')
                
            if invalid:
                html = render_template(
                    'add.html',      
                    page_type='new',
                    form_meta={'action':'/add?edit', 'method':'POST'},
                    form_data=form_data,
                    invalid=invalid
                )
                return html

            else:
                form_data['Activity Name'] = form_data['Activity Name'].title()
                form_data['Description'] = form_data['Description'].capitalize()
                        
                
        html = render_template(
            'add.html',
            page_type='confirm',
            form_meta={'action':'/add?success', 'method':'POST'},
            form_data=form_data,
        )

    elif 'edit' in request.args:#Editing input 
        html = render_template(
            'add.html',
            page_type='new',
            form_meta={'action':'/add?confirm', 'method':'POST'},
            form_data=form_data,
        )

    else:        #insertion into database
        record = {}
        
        if form_data['type'] == 'Club':
            name = form_data['Club Name']
            record = {'name': name}
            ClubDB.insert(record) # Insert record into Club database
            
        else:
            name = form_data['Activity Name'].title()
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
            form_meta={'action':'/view?search', 'method':'POST'},
        )
        
    elif 'search' in request.args:      # After selection of category
        if form_data['type'] == 'Student':
            form_data['Student Name'] = ''
        elif form_data['type'] == 'Class':
            form_data['Class Name'] = ''
        elif form_data['type'] == 'Club':
            form_data['Club Name'] = ''
        else:
            form_data['Activity Name'] = ''
        
        html = render_template(
            'view.html',
            page_type='search',
            form_meta={'action':'/view?result', 'method':'POST'},
            form_data=form_data,
        )

    elif 'result' in request.args:        # After input of data to be searched
        if form_data['type'] == 'Student':     # If item to be searched is 'Student'
            student_name = form_data['Student Name'].upper()
            
            if validate.name(student_name):   # Validation
                data = StudentDB.find(student_name)
                
                if data is not None:  # Record present
                    form_data['Age'] = data[2]
                    form_data['Year enrolled'] = data[3]
                    form_data['Graduating year'] = data[4]
                    form_data['Class'] = data[5]
                    
                else:   # Record not present
                    html = render_template(
                        'view.html', 
                        page_type='/view?search',
                        form_meta={'action':'/view?result', 'method':'POST'},
                        form_data=form_data,
                        invalid=['Student Name']
                    )
                    return html
                
            else:   # Validation failure
                html = render_template(
                    'view.html', 
                    page_type='/view?search',
                    form_meta={'action':'/view?result', 'method':'POST'},
                    form_data=form_data,
                    invalid={'Student Name':'Input is invalid'}
                )
                return html
                
        elif form_data['type'] == 'Class':   # If item to be searched is 'Class'
            class_name = form_data['Class Name']
            
            if validate.class_name(class_name):   # Validation
                data = ClassDB.find(class_name)

                if data is not None:   # Record present
                    form_data['Level'] = data[2]
                    
                else:    # Record not present
                    html = render_template(
                        'view.html', 
                        page_type='/view?search',
                        form_meta={'action':'/view?result', 'method':'POST'},
                        form_data=form_data,
                        invalid={'Class Name':'Cannot be found'}
                    )
                    return html
                
            else:   # Validation failure
                html = render_template(
                    'view.html', 
                    page_type='/view?search',
                    form_meta={'action':'/view?result', 'method':'POST'},
                    form_data=form_data,
                    invalid={'Class Name':'Input is invalid'}
                )
                return html
                
        elif form_data['type'] == 'Club':    # If item to be searched is 'Club'
            club_name = form_data['Club Name'].title()
            
            if validate.name(club_name):    # Validation
                data = ClubDB.find(club_name)
                
                if data is not None:   # Record present
                    form_data['id'] = data[0]
                    
                else:    # Record not present
                    html = render_template(
                        'view.html', 
                        page_type='/view?search',
                        form_meta={'action':'/view?result', 'method':'POST'},
                        form_data=form_data,
                        invalid={'Club Name':'Cannot be found'}
                    )
                    return html
                
            else:   # Validation failure
                html = render_template(
                    'view.html', 
                    page_type='/view?search',
                    form_meta={'action':'/view?result', 'method':'POST'},
                    form_data=form_data,
                    invalid={'Club Name':'Input is invalid'}
                )
                return html
              
        else:   # If item to be searched is 'Activity'
            activity_name = form_data['Activity Name']
            
            if validate.name(activity_name):  # Validation
                data = ActivityDB.find(activity_name)

                if data is not None:   # Record present
                    form_data['Start Date'] = data[2]
                    form_data['End Date'] = data[3]
                    form_data['Description'] = data[4]
                    
                else:     # Record not present
                    html = render_template(
                        'view.html', 
                        page_type='/view?search',
                        form_meta={'action':'/view?result', 'method':'POST'},
                        form_data=form_data,
                        invalid={'Activity Name':'Cannot be found'}
                    )
                    return html
                
            else:   # Validation failure
                html = render_template(
                    'view.html', 
                    page_type='/view?search',
                    form_meta={'action':'/view?result', 'method':'POST'},
                    form_data=form_data,
                    invalid={'Activity Name':'Input is invalid'}
                )
                return html

        html = render_template(     #?????????
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

    if len(request.args) == 0:   # First entry into /edit
        html = render_template(
            'edit.html',
            page_type='edit',
            form_meta={'action':'/edit?search', 'method':'POST'},
        )

    elif 'search' in request.args:    # After selection of category
        form_data['Student Name'] = ''
        form_data['Club Name'] = ''
        
        if form_data['type'] == 'Participation':
            form_data['Activity Name'] = ''
        
        html = render_template(
            'edit.html',
            page_type='search',
            form_meta={'action':'/edit?result', 'method':'POST'},
            form_data=form_data,
        )
    
    elif 'result' in request.args:    # Search database
        form_data['Student Name'] = form_data['Student Name'].upper()
        student_name = form_data['Student Name']
        form_data['Club Name'] = form_data['Club Name'].title()
        club_name = form_data['Club Name']
        invalid = []

        if not validate.name(student_name): # Validation 
            invalid.append('Student Name')
        if not validate.name(club_name):
            invalid.append('Club Name')

        if form_data['type'] == 'Participation': # Validate for activity name in participation
            form_data['Activity Name'] = form_data['Activity Name'].title()
            activity_name = form_data['Activity Name']
            
            if not validate.name(activity_name):
                invalid.append('Activity Name')

        # breakpoint()

        if invalid:
            html = render_template(
                'edit.html',      
                page_type='search',
                form_meta={'action':'/edit?result', 'method':'POST'},
                form_data=form_data,
                invalid=invalid
            )
            return html
        
        student_id = StudentDB.findID(student_name)
        club_id = ClubDB.findID(club_name)

        absent = []
        if student_id is None: # Check if student exists in db
            absent.append('Student Name')

        if club_id is None:
            absent.append('Club Name')

        if form_data['type'] == 'Participation': # Validate for activity name in participation
            activity_id = ActivityDB.findID(activity_name)
            if activity_id is None:
                absent.append('Activity Name')

        if absent:
            html = render_template(
                'edit.html',      
                page_type='search',
                form_meta={'action':'/edit?result', 'method':'POST'},
                form_data=form_data,
                absent=absent
            )
            return html
                
        if form_data['type'] == 'Membership':
            membership_data = MembershipDB.find(student_id, club_id)
            
            if membership_data is not None: # Checks if membership in db
                form_data['Role'] = membership_data[2]

                html = render_template(
                    'edit.html',
                    page_type='result',
                    form_meta={'action':'edit?confirm', 'method':'POST'},
                    form_data=form_data,
                )
                return html     

            # else:
            #     html = render_template(
            #         'edit.html',
            #         page_type='edit?error',
            #         form_data=form_data,
            #     )
                
        else:            
            participation_data = ParticipationDB.find(student_id, club_id, activity_id)

            if participation_data is not None: # Checks if the participation exists in db
                form_data['Category'] = participation_data[2]
                form_data['Role'] = participation_data[3]
                form_data['Award'] = participation_data[4]
                form_data['Hours'] = participation_data[5]
        
                html = render_template(
                    'edit.html',
                    page_type='result',
                    form_meta={'action':'edit?confirm', 'method':'POST'},
                    form_data=form_data,
                )
                return html   
                
            # else:
            #     form_data['Activity Name'] = 'Cannot be Found'
            #     html = render_template(
            #         'edit.html',
            #         page_type='result',
            #         form_meta={'action':'edit?search', 'method':'POST'},
            #         form_data=form_data,
            #     )


            #     else:
            #         html = render_template(
            #             'edit.html',
            #             page_type='edit?error',
            #             form_data=form_data,
            #         )


    elif 'confirm' in request.args:
        student_name = form_data['Student Name']
        club_name = form_data['Club Name']
        
        student_id = StudentDB.findID(student_name)        
        club_id = ClubDB.findID(club_name)
        old_data = {}

        if form_data['type'] == 'Membership':
            curr_data = MembershipDB.find(student_id, club_id)
        else:
            activity_name = form_data['Activity Name']
            activity_id = ActivityDB.findID(activity_name)
            curr_data = ParticipationDB.find(student_id, club_id, activity_id)

        """Change tuple to dictionary"""
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

        html = render_template(
            'edit.html',
            page_type='confirm',
            form_meta={'action':'edit?success','method':'POST'},
            form_data=form_data,
            old_data = old_data,
        )
        
    else:
        role = form_data['Role']
        student_name = form_data['Student Name']
        club_name = form_data['Club Name']
        student_id = StudentDB.findID(student_name)
        club_id = ClubDB.findID(club_name)
        
        if form_data['type'] == 'Membership':
            Membership.update(role, student_id, club_id)
            
        else:
            activity_name = form_data['Activity Name']
            activity_id = ActivityDB.findID(activity_name)
            category = form_data['Category']
            award = form_data['Award']
            hours = form_data['Hours']            
            ParticipationDB.update(category, role, award, hours, student_id, club_id, activity_id) 

        name = list(form_data.values())[1]
        html = render_template(
            'edit.html',
            page_type='success',
            name=name,
            type=type,
        )

    return html


app.run(host='0.0.0.0', port=8080)