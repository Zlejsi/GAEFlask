"""
Routes and views for the flask application.
"""
import uuid
from datetime import datetime
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
    
@app.route('/local/clubs', methods=['GET','POST'])
def clubs():
    """Renders the clubs page."""
    clubs = Clubs.query.all()
    return render_template(
        'clubs.html',
        title='Create Club', clubs = clubs
    )