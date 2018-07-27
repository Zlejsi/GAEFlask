from datetime import datetime
from SportsWebPython import db
from SportsWebPython.models.basemodel import BaseModel,GUID

class User(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20),nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post',backref='author',lazy=True)

    def __repr__(self):
        return  "'{0}' {1}".format(self.username,self.email)


class Post(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)

    def __repr__(self):
        return  "'{0}' {1}".format(self.title,self.content)

class Persons(BaseModel):
    Id_Person = db.Column(db.Integer, primary_key=True)
    First_name = db.Column(db.String(50), nullable=False)
    Second_name = db.Column(db.String(50), nullable=True)
    Surname = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(120), nullable=True)
    Photo = db.Column(db.LargeBinary(length=(2**32)-1))
    #photo_data = db.Column(db.LargeBinary,nullable=True)
    Height = db.Column(db.Float, nullable=True)
    Weight = db.Column(db.Float, nullable=True)
    
    _default_fields = [
        "Id_person",
        "First_name",
        "Second_name",
        "Surname",
        "Email",
        "Height",
        "Weight"
    ]

    def __repr__(self):
        return  "'{0}' {1}".format(self.first_name,self.second_name)

class Members(BaseModel):
    Id_Member = db.Column(db.Integer, primary_key=True)   
    Id_Person = db.Column(db.Integer, db.ForeignKey('persons.Id_Person'),nullable=False)
    Id_Club = db.Column(db.Integer, db.ForeignKey('clubs.Id_Club'),nullable=False)
    Id_Team = db.Column(db.Integer, db.ForeignKey('teams.Id_Team'),nullable=False)
    Date_Of = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    Nickname = db.Column(db.String(50), nullable=True)
    Date_To = db.Column(db.DateTime, nullable=True)
    Id_Position = db.Column(db.Integer, db.ForeignKey('positions.Id_Position'),nullable=False)
    person = db.relationship('Persons', uselist=False)
    position = db.relationship('Positions',uselist=False)
    def __repr__(self):
        return  "'{0}'".format(self.Id_Member)

class Clubs(BaseModel):
    Id_Club = db.Column(db.Integer, primary_key=True)   
    Name = db.Column(db.String(100), nullable=False)
    #logo = db.Column(db.String(20),nullable=True, default='default.jpg')
    Logo = db.Column(db.LargeBinary(length=(2**32)-1))
    Since = db.Column(db.Integer, nullable=True)
    Date_Of = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    Date_To = db.Column(db.DateTime, nullable=True)
    teams = db.relationship('Teams',backref='teams',lazy=True)

    _default_fields = [
        "Id_Club",
        "Name",
        "Since",
        "Date_Of",
        "Date_To",
        "teams"    
    ]

    def __repr__(self):
        return  "'{0}' '{1}' {2} {3}".format(self.Name,self.Since,self.Date_Of,self.Date_To)

class Teams(BaseModel):
    Id_Team = db.Column(db.Integer, primary_key=True) 
    Id_Club = db.Column(db.Integer, db.ForeignKey('clubs.Id_Club'),nullable=False,unique=False)  
    Name = db.Column(db.String(100), nullable=False)
    Date_Of = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    Date_To = db.Column(db.DateTime, nullable=True)
    members = db.relationship('Members',backref='members',lazy=True)

    _default_fields = [
        "Id_Team",
        "Id_Club",
        "Name",
        "Date_Of",
        "Date_To",
        "members"    
    ]

    def __repr__(self):
        return  "'{0}'".format(self.Name)


class Positions(BaseModel):
    Id_Position = db.Column(db.Integer, primary_key=True)   
    Name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return  "'{0}'".format(self.Name)

class Events(BaseModel):
    Id_Event = db.Column(db.Integer, primary_key=True)
    Id_Team = db.Column(db.Integer, db.ForeignKey('teams.Id_Team'), nullable=False)
    Id_Batch = db.Column(db.Integer, nullable=True)
    Subject = db.Column(db.String(100), nullable=False)
    Description = db.Column(db.String(4000), nullable=True)
    Date_Start = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    Date_End = db.Column(db.DateTime, nullable=True)

    _default_fields = [
        "Id_Event",
        "Id_Team",
        "Id_Batch",
        "Subject",
        "Description",
        "Date_Start",
        "Date_End"
        
    ]