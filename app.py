from flask import Flask,jsonify,render_template,request,url_for,redirect
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate

from flask_bcrypt import Bcrypt
from flask_cors import CORS
import os 
# import .models

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
CORS(app)
ENV = 'prod'
if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:3050manu@localhost/flap'
else:
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
migrate = Migrate(app,db)
bcrypt = Bcrypt(app)
import datetime
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self,email,password,admin=False):
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password
            # ,app.config.get('BCRYPT_LOG_ROUNDS')
        )
        self.registered_on = datetime.datetime.now()
        self.admin = admin
class Products(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(200))
    price = db.Column(db.String(200))
    desc = db.Column(db.Text())
    def __init__(self,name,price,desc):
        self.name = name
        self.price = price
        self.desc = desc
@app.route('/',methods=["GET","POST"])
def index():
    products = Products.query.all()
    print(products)
    return render_template('index.html',products=products)
@app.route('/add',methods=["GET","POST"])
def adda():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        desc = request.form['desc']
        print(name)
        product =  Products(
            name,price,desc
        )
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('index'))

@app.route('/product/<int:id>/',methods=["GET","PUT"])
def single(id):
    product = db.session.query(Products).filter(Products.id==id)
    product = product.first()
    print(product)
    db.session.delete(product)
    db.session.commit()
    print("delete")
    return render_template('product.html',product=product)

if __name__ == "__main__":
    print(os.getenv("DATABASE_URL"))
    
    app.run()

