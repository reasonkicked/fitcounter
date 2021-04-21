from flask import Flask, render_template, request, redirect, url_for, flash
import pdb
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://fitcounter:CluLnxPa$$@192.168.1.131:5432/fitcounterdb"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class CarsModel(db.Model):
    __tablename__ = 'cars'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    model = db.Column(db.String())
    doors = db.Column(db.Integer())

    def __init__(self, name, model, doors):
        self.name = name
        self.model = model
        self.doors = doors

    def __repr__(self):
        return f"<Car {self.name}>"


@app.route('/cars', methods=['POST', 'GET'])
def handle_cars():
    if request.method == 'POST':
        name = request.form.get("title")
        model = request.form.get("description")
        new_car = CarsModel(name=name, model=model, doors=4)
        db.session.add(new_car)
        db.session.commit()
        return render_template("cars.html")

    elif request.method == 'GET':
        cars = CarsModel.query.all()
        results = [
            {
                "name": car.name,
                "model": car.model,
                "doors": car.doors
            } for car in cars]

        # return {"count": len(results), "cars": results}
        return render_template("cars.html", results=results)


@app.route('/cars/<car_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_car(car_id):
    car = CarsModel.query.get_or_404(car_id)

    if request.method == 'GET':
        response = {
            "name": car.name,
            "model": car.model,
            "doors": car.doors
        }
        return render_template("modify_car.html", response=response)

    elif request.method == 'POST':
        name = request.form.get("title")
        model = request.form.get("description")
        new_car = CarsModel(name=name, model=model, doors=4)
        db.session.add(new_car)
        db.session.commit()
        return render_template("modify_car.html")

    elif request.method == 'PUT':
        data = request.get_json()
        car.name = data['name']
        car.model = data['model']
        car.doors = data['doors']
        db.session.add(car)
        db.session.commit()
        return {"message": f"car {car.name} successfully updated"}

    elif request.method == 'DELETE':
        db.session.delete(car)
        db.session.commit()
        return {"message": f"Car {car.name} successfully deleted."}


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/item/new", methods=["GET", "POST"])
def new_item():
    if request.method == "POST":
        # Process the form data
        print("Form data:")
        print("Title: {}, Description: {}".format(
            request.form.get("title"), request.form.get("description")
        ))
        # redirect to some page
        return redirect(url_for("home"))

    return render_template("new_item.html")





if __name__ == "__main__":
    home()
    #  print("File one executed when ran directly")