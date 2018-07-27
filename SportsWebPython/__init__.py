"""
The flask application package.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
#test
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/SportDB'
#production
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@/SportDB?unix_socket=/cloudsql/aerial-chimera-211120:europe-west2:sporteventdb'
db = SQLAlchemy(app)

#Instance connection name: aerial-chimera-211120:europe-west2:sporteventdb
#Instance ID : sporteventdb
#mysql+mysqldb://root@/<dbname>?unix_socket=/cloudsql/<projectid>:<instancename>



   
import views
