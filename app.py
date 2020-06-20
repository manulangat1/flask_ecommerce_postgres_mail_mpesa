from flask import Flask,jsonify,render_template
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate
import os 
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app,db)

ENV = 'DEV'
if ENV == 'DEV':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
else:
    pass




@app.route('/',methods=["GET","POST"])
def index():
    return "Hello world"


if __name__ == "__main__":
    app.debug = True
    app.run(port=4000)

