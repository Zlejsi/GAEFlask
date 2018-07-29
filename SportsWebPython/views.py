"""
Routes and views for the flask application.
"""
import uuid
from datetime import datetime
import dateutil.parser
import json
from flask import render_template,redirect,url_for,request,jsonify,flash
from SportsWebPython import app,db
from SportsWebPython.models.models import User,Clubs,Persons,Events,Teams,Members
from SportsWebPython.forms.forms import CreateClubForm,PersonForm,EventForm,TeamForm

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'layout2.html'
    )
    
@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )
    
@app.route('/local/club', methods=['GET','POST'])
def createclub():
    """Renders the create club page."""
    form = CreateClubForm()
    if form.validate_on_submit():
        file = request.files.get('Logo')
        #file = request.files['Logo']
        if file:
            logo = file.read()
        else:
            logo = None
        club = Clubs(UID=uuid.uuid4(),Name=form.Name.data,Since=form.Since.data,Date_Of=form.Date_Of.data,Logo=logo)
        db.session.add(club)
        db.session.commit()
        return redirect(url_for('home'))
        flash('Club succesfully created', 'success')
    return render_template(
        'club.html',
        title='Create Club', form = form
    )

@app.route('/local/club<int:clubId>/logo')
def club_logo(clubId):
    club = Clubs.query.get_or_404(clubId)
    return app.response_class(club.Logo, mimetype='application/octet-stream') 
    
@app.route('/local/clubs', methods=['GET','POST'])
def clubs():
    """Renders the clubs page."""
    clubs = Clubs.query.all()
    return render_template(
        'clubs.html',
        title='Create Club', clubs = clubs
    )

@app.route('/local/team<int:clubId>', methods=['GET','POST'])
def createteam(clubId):
    """Renders the create club page."""
    form = TeamForm()
    if form.validate_on_submit():
        team = Teams(UID=uuid.uuid4(),Id_Club=clubId, Name=form.Name.data,Date_Of=form.Date_Of.data)
        db.session.add(team)
        db.session.commit()
        return redirect(url_for('clubs'))
        flash('Team succesfully created', 'success')
    return render_template(
        'team.html',
        title='Create Team', form = form
    )
    
@app.route('/local/team<int:teamId>/members', methods=['GET','POST'])
def editteam(teamId):
    """Renders the create club page."""

    team = Teams.query.get(teamId)
    #if form.validate_on_submit():
    #    member = Members(UID=uuid.uuid4(),Id_Club=clubId, Name=form.Name.data,Date_Of=form.Date_Of.data)
    #    db.session.add(member)
    #    db.session.commit()
        #return redirect(url_for('clubs'))
        #flash('Team succesfully created', 'success')
    return render_template(
        'editTeam.html',
        title='Edit Team', team=team
    )

@app.route('/local/persons', methods=['GET'])
def persons():
    """Renders the persons page."""
    persons = Persons.query.all() 
    return render_template(
        'persons.html',
        title='Persons', persons = persons
    )
        
@app.route('/local/person<int:personId>/logo')
def person_photo(personId):
    person = Persons.query.get_or_404(personId)
    return app.response_class(person.Photo, mimetype='application/octet-stream')

@app.route('/local/person', methods=['GET','POST'])
def createperson():
    """Renders the create person page."""
    form = PersonForm()
    data_type = 'Create Person'
    if form.validate_on_submit():
        file = request.files['Photo']
        person = Persons(First_name=form.First_name.data,
                        Second_name=form.Second_name.data,
                        Surname=form.Surname.data,
                        Photo=file.read(),
                        Email=form.Email.data,
                        Height=form.Height.data,
                        Weight=form.Weight.data,
                        UID=uuid.uuid4()
                        )
        db.session.add(person)
        db.session.commit()
        flash('Person succesfully created', 'success')
        return redirect(url_for('persons'))
    return render_template(
        'createPerson.html',
        title='Create Person', form = form,data_type=data_type
    )

@app.route('/local/person<string:uid>', methods=['GET','POST'])
def editperson(uid):
    """Renders the create person page."""
    person = Persons.query.filter_by(UID=uid).first()
    form = PersonForm(obj=person)
    data_type='Update Person'
    if form.validate_on_submit():
        file = request.files['Photo']
        form.populate_obj(person)
        person.Photo=file.read()
        db.session.add(person)
        db.session.commit()
        #person.put()
        flash('Person succesfully updated', 'success')
    #form.first_name.data = person.First_name
    return render_template(
        'createPerson.html',
        title='Update Person', form = form,person=person,data_type=data_type
    )
    
@app.route('/local/personsModal/<int:teamId>', methods=['GET','POST'])
def addmember(teamId):
    """Renders the event modal page."""
    persons = Persons.query.all();
    team = Teams.query.filter_by(Id_Team=teamId).first();
    #form = EventForm(obj=event)
    #data_type='Update Event'

    #if (request.method == 'POST'):
    #    if 'Subject' in request.form:
    #        event.Subject = request.form['Subject'];
    #    if 'Description' in request.form:
    #        event.Descrition = request.form['Description'];
    #    if 'Date_Start' in request.form:
    #        event.Date_Start = dateutil.parser.parse(request.form['Date_Start']);
    #    if 'Date_End' in request.form:
    #        event.Date_End = dateutil.parser.parse(request.form['Date_End']);
    #    db.session.add(event);
    #    db.session.commit();

    #    return json.dumps(event.to_dict())
    return render_template(
        'personsModal.html',
        title='Add members',persons=persons,team=team
    )

@app.route('/local/team<int:teamId>/members/add', methods=['GET','POST'])
def addteammembers(teamId):
    """Renders the event modal page."""
    team = Teams.query.filter_by(Id_Team=teamId).first();

    if request.method == 'POST':
        for id in request.get_json()["ids"]:
            member = Members(UID=uuid.uuid4(),Id_Person=id,Id_Team=teamId,Id_Club=team.Id_Club,Id_Position=1);
            db.session.add(member);
        db.session.commit();

        return redirect(url_for('editteam',teamId=teamId))
    #form = EventForm(obj=event)
    #data_type='Update Event'

    #if (request.method == 'POST'):
    #    if 'Subject' in request.form:
    #        event.Subject = request.form['Subject'];
    #    if 'Description' in request.form:
    #        event.Descrition = request.form['Description'];
    #    if 'Date_Start' in request.form:
    #        event.Date_Start = dateutil.parser.parse(request.form['Date_Start']);
    #    if 'Date_End' in request.form:
    #        event.Date_End = dateutil.parser.parse(request.form['Date_End']);
    #    db.session.add(event);
    #    db.session.commit();

    #    return json.dumps(event.to_dict())
    return json.dumps([])

@app.route('/calendar', methods=['GET','POST'])
def calendar():
    """Renders the calendar page."""
    #event = Events(Id_Team=1,Subject='Prvni trenink',Date_Start=datetime.utcnow)


    return render_template(
        'calendar.html',
        title='Calendar'
    )

@app.route('/events', methods=['GET','POST'])
def events():
    """Renders the calendar page."""
    #event = Events(Id_Team=1,Subject='Prvni trenink',Date_Start=datetime.utcnow())
    events = Events.query.all()
    dict3 = []
    for event in events:
        dict = event.to_dict()
        dict.update({'title': dict['Subject'],'start':dict['Date_Start'], 'id': dict['Id_Event'],'end':dict['Date_End']})
        if event.Id_Team == 1:
            dict.update({'backgroundColor':'red'})
        else: 
            dict.update({'backgroundColor':'blue'}) 
        dict3.append(dict)

    return json.dumps(dict3)

@app.route('/local/event/', methods=['GET','POST'])
def addevent():
    """Renders the event modal page."""
    #event = Events.query.filter_by(Id_Event=uid).first()
    form = EventForm()
    data_type='Add Event'
    teams = Teams.query.all()

    if (request.method == 'POST'):
        event = Events(UID = uuid.uuid4(), Id_Team = 1, Subject = request.form['Subject'],Description = request.form['Description'], Date_Start = dateutil.parser.parse(request.form['Date_Start']))
        db.session.add(event);
        db.session.commit();

        return json.dumps(event.to_dict())
    return render_template(
        'event.html',
        title='Add event', form=form,data_type=data_type, teams=teams
    )
    
@app.route('/local/event/<string:uid>', methods=['GET','POST'])
def editevent(uid):
    """Renders the event modal page."""
    event = Events.query.filter_by(Id_Event=uid).first()
    form = EventForm(obj=event)
    data_type='Update Event'
    teams = Teams.query.all()
    if (request.method == 'POST'):
        if 'Subject' in request.form:
            event.Subject = request.form['Subject'];
        if 'Description' in request.form:
            event.Descrition = request.form['Description'];
        if 'Date_Start' in request.form:
            event.Date_Start = dateutil.parser.parse(request.form['Date_Start']);
        if 'Date_End' in request.form:
            event.Date_End = dateutil.parser.parse(request.form['Date_End']);
        if 'teamId' in request.form:
            event.Id_Team = request.form['teamId'];
        db.session.add(event);
        db.session.commit();

        return json.dumps(event.to_dict())
    return render_template(
        'event.html',
        title='Update event', form = form,event=event,data_type=data_type, teams=teams
    )
