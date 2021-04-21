from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
import pdb
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://fitcounter:CluLnxPa$$@192.168.1.131:5432/fitcounterdb"
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class MealsModel(db.Model):
    __tablename__ = 'meals'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    description = db.Column(db.String())
    price = db.Column(db.Float())

    def __init__(self, title, description, price):
        self.title = title
        self.description = description
        self.price = price

    def __repr__(self):
        return f"<meal {self.title}>"


class DeleteMealForm(FlaskForm):
    submit = SubmitField("Delete item")


@app.route('/new_meal', methods=['POST', 'GET'])
def handle_meals():
    if request.method == 'POST':
        title = request.form.get("title")
        description = request.form.get("description")
        new_meal = MealsModel(title=title, description=description, price=4)
        db.session.add(new_meal)
        db.session.commit()
        return render_template("new_meal.html")

    elif request.method == 'GET':
        meals = MealsModel.query.all()
        results = [
            {
                "name": meal.title,
                "model": meal.description,
                "doors": meal.price
            } for meal in meals]

        # return {"count": len(results), "meals": results}
        return render_template("new_meal.html", results=results)


@app.route('/meals/<meal_id>', methods=['POST', 'GET', 'PUT', 'DELETE'])
def handle_meal(meal_id):
    meal = MealsModel.query.get_or_404(meal_id)

    if request.method == 'GET':
        response = {
            "title": meal.title,
            "description": meal.description,
            "price": meal.price
        }

        return render_template("modify_meal.html", meal_id=meal_id, response=response)

    elif request.method == 'POST':
        meal.title = request.form.get("title")
        meal.description = request.form.get("description")
        meal.price = request.form.get("price")

        db.session.commit()
        return render_template("modify_meal.html")

    return redirect(url_for("home"))

@app.route('/meal/<meal_id>', methods=['GET'])
def view_meal(meal_id):
    meal = MealsModel.query.get_or_404(meal_id)
    if request.method == 'GET':
        response = {
            "title": meal.title,
            "description": meal.description,
            "price": meal.price
        }
        return render_template("meal.html", meal_id=meal_id, response=response)


@app.route('/meal<int:meal_id>/delete', methods=["POST", "GET"])
def delete_meal(meal_id):
    meal = MealsModel.query.get_or_404(meal_id)

    deleteMealForm = DeleteMealForm()

    db.session.delete(meal)
    db.session.commit()
    return render_template()


@app.route("/")
def home():
    return render_template("home.html")


