import os
base_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(base_dir, "foods.sqlite"))

from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)

##------Models------##
class FoodCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), unique=True)
    foods = db.relationship('Food', backref="whatType")

    def __repr__(self):
        return '<FoodCat %r>' %self.name

class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), unique=True, index=True, nullable=False)
# FOREIGN KEY
    food_type = db.Column(db.Integer, db.ForeignKey("food_category.id"))

    def __repr__(self):
        return '<Food %r>' %self.name

##------Routes------##
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/echo')
def echo():
    to_echo = request.args.get("echo","")
    response = "{}".format(to_echo)
    return response
@app.route('/graph')
def graph():
    foodcat = FoodCategory.query.all()
    ##-----Debugging-----##
    print(type(foodcat))
    return render_template('graph.html', graph = foodcat)

@app.route('/shock')
def hero():
    return app.send_static_file('superhero.html')

app.run(port=5050,debug=True)

