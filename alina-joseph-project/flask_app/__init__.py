from flask import Flask
from flask import flash
from flask_bcrypt import Bcrypt  

app = Flask(__name__)
app.secret_key= "keep it secreto"