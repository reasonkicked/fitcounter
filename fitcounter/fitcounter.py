from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField, DecimalField
from wtforms.validators import InputRequired, DataRequired, Length

import pdb
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import os

app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://fitcounter:CluLnxPa$$@192.168.1.131:5432/fitcounterdb"
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class MealsModel(db.Model):
    __tablename__ = 'meals'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    description = db.Column(db.String())
    price = db.Column(db.Float())
    category = db.Column(db.String())
    subcategory = db.Column(db.String())

    def __init__(self, title, description, price, category, subcategory):
        self.title = title
        self.description = description
        self.price = price
        self.category = category
        self.subcategory = subcategory

    def __repr__(self):
        return f"<meal {self.title}>"


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


class Subategory(db.Model):
    __tablename__ = 'subcategories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    category_id = db.Column(db.Integer())

    def __init__(self, name, category_id):
        self.name = name
        self.category_id = category_id

    def __repr__(self):
        return self.name


class NewItemForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired("Input is required!"),
                                             DataRequired("Data is required!"),
                                             Length(min=2, max=20,
                                                    message="Input must be between 5 and 20 characters long!")])
    price = DecimalField("Price")
    description = TextAreaField("Description", validators=[InputRequired("Input is required!"),
                                                           DataRequired("Data is required!"),
                                                           Length(min=2, max=50,
                                                                  message=
                                                                  "Input must be between 2 and 50 characters long!")])
    category = SelectField("Category")
    subcategory = SelectField("Subcategory")
    submit = SubmitField("Submit")


class DeleteMealForm(FlaskForm):
    submit = SubmitField("Delete item")


@app.route('/new_meal', methods=['POST', 'GET'])
def handle_meals():
    form = NewItemForm()
    categories = Category.query.all()
    subcategories = Subategory.query.all()
    form.category.choices = categories
    form.subcategory.choices = subcategories

    if form.validate_on_submit():
        if request.method == 'POST':
            title = request.form.get("title")
            description = request.form.get("description")
            price = request.form.get("price")
            category = request.form.get("category")
            subcategory = request.form.get("subcategory")
            new_meal = MealsModel(title=title, description=description, price=price, category=category,
                                  subcategory=subcategory)
            db.session.add(new_meal)
            db.session.commit()

            flash("Meal {} has been successfully submitted".format(request.form.get("title")), "success")
            return redirect((url_for("home")))

    if form.errors:
        flash("{}".format(form.errors), "danger")
    return render_template("new_meal.html", form=form)


@app.route('/meals/<meal_id>', methods=['POST', 'GET', 'PUT', 'DELETE'])
def handle_meal(meal_id):
    meal = MealsModel.query.get_or_404(meal_id)
    form = NewItemForm()
    categories = Category.query.all()
    subcategories = Subategory.query.all()
    form.category.choices = categories
    form.subcategory.choices = subcategories

    if request.method == 'GET':

        return render_template("modify_meal.html", meal_id=meal.id, form=form)

    elif request.method == 'POST':
        meal.title = request.form.get("title")
        meal.description = request.form.get("description")
        meal.price = request.form.get("price")

        db.session.commit()
        return redirect(url_for("home"))

    return redirect(url_for("home"))


@app.route('/meal/<meal_id>', methods=['GET'])
def view_meal(meal_id):
    meal = MealsModel.query.get_or_404(meal_id)
    if request.method == 'GET':
        response = {
            "title": meal.title,
            "description": meal.description,
            "price": meal.price,
            "category": meal.category,
            "subcategory": meal.subcategory
        }
        delete_meal_form = DeleteMealForm()
        return render_template("meal.html", meal=meal, delete_meal_form=delete_meal_form, response=response)


@app.route('/meal<int:meal_id>/delete', methods=["POST", "GET"])
def delete_meal(meal_id):
    meal = MealsModel.query.get_or_404(meal_id)

    delete_meal_form = DeleteMealForm()

    db.session.delete(meal)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/")
def home():
    items_from_db = []
    meals = MealsModel.query.all()
    for meal in meals[:10]:
        items_from_db.append(meal)
    return render_template("home.html", meals=meals)
