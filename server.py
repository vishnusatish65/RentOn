from flask import Flask
from user import user
from properties import properties
from flask_mysqldb import MySQL
import jwt
import os

app = Flask(__name__)

# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = os.environ.get('DB_PASS')
# app.config['MYSQL_DB'] = 'practise'

app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(properties, url_prefix='/properties')
 
# mysql = MySQL(app)

@app.route('/')
def home():
    return 'Welcome to RentOn'
