from datetime import datetime
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField,SubmitField,BooleanField,DateField,DecimalField,IntegerField,TextAreaField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError 
from SportsWebPython.models.models import User,Clubs,Persons


class CreateClubForm(FlaskForm):
    Name = StringField('Name',validators=[DataRequired()])
    Logo = FileField('Club logo',id='imgInp', validators=[FileAllowed(['jpg','png'])])
    Since = IntegerField('Since')
    Date_Of = DateField('Date of',format="%d.%m.%Y",default=datetime.today)
    Submit = SubmitField('Create club')

    def validate_name(self, name):
        club = Clubs.query.filter_by(Name=name.data).first()
        if club:
            raise ValidationError('Club already exist')

class TeamForm(FlaskForm):
    Name = StringField('Name',validators=[DataRequired()])
    Date_Of = DateField('Date of',format="%d.%m.%Y",default=datetime.today)
    Submit = SubmitField('Create team')

    def validate_name(self, name):
        club = Clubs.query.filter_by(Name=name.data).first()
        if club:
            raise ValidationError('Club already exist')

class PersonForm(FlaskForm):
    First_name = StringField('First_Name',validators=[DataRequired()])
    Second_name = StringField('Second_Name')
    Surname = StringField('Surname',validators=[DataRequired()])
    Email = StringField('Email',validators=[Email()])
    Photo = FileField('Photo',id='imgInp', validators=[FileAllowed(['jpg','png'])])
    Weight = DecimalField('Weight')
    Height = DecimalField('Height')
    Submit = SubmitField('Create Person')

    #def validate_name(self, First_name):
    #    person = Persons.query.filter_by(First_name=First_name.data).first()
    #    if person:
    #        raise ValidationError('Person already exist')

class EventForm(FlaskForm):
    Subject = StringField('Subject',validators=[DataRequired()])
    Description = TextAreaField('Description')
    #Date_Start = DateField('Date Start',format="%d.%m.%Y",default=datetime.today)
    #Date_End = DateField('Date End',format="%d.%m.%Y")
    Submit = SubmitField('Edit Event')

