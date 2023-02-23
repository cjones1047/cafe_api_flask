import sqlalchemy.exc
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/CaseyJr/Dropbox/100_days_of_python/cafe_api_flask/cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/random")
def random_cafe():
    cafes = db.session.query(Cafe).all()
    random_cafe_choice = random.choice(cafes)

    return jsonify(cafe=random_cafe_choice.to_dict())


@app.route("/all")
def all_cafes():
    cafes = db.session.query(Cafe).all()

    return jsonify(cafes=[cafe.to_dict() for cafe in cafes])


@app.route("/search")
def search_cafe_by_location():
    searched_location = request.args.get("loc").title()
    cafes_in_location = db.session.query(Cafe).filter(Cafe.location == searched_location)
    if cafes_in_location.count() > 0:
        return jsonify(cafes_in_location=[cafe.to_dict() for cafe in cafes_in_location])

    return jsonify(
        error={"Not found": "Sorry, we don't have a cafe in that location."}
    )


@app.route("/add")
def add_cafe():
    # new_cafe = Cafe(
    #     name=request.form['name'],
    #     map_url=request.form['map_url'],
    #     img_url= db.Column(db.String(500), nullable=False)
    #     location= db.Column(db.String(250), nullable=False)
    #     seats = db.Column(db.String(250), nullable=False)
    #     has_toilet = db.Column(db.Boolean, nullable=False)
    #     has_wifi = db.Column(db.Boolean, nullable=False)
    #     has_sockets = db.Column(db.Boolean, nullable=False)
    #     can_take_calls = db.Column(db.Boolean, nullable=False)
    #     coffee_price = db.Column(db.String(250), nullable=True)
    # )
    cafe_dict = dict(request.form)
    for key, value in cafe_dict.items():
        if value.lower() == 'true':
            cafe_dict[key] = True
        elif value.lower() == 'false':
            cafe_dict[key] = False
    new_cafe = Cafe(**cafe_dict)
    db.session.add(new_cafe)
    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as error_message:
        return jsonify(error={"Could not add cafe": f"{str(error_message)}"})

    return jsonify(success={"success": f"Successfully added cafe: {cafe_dict['name']}"})


## HTTP GET - Read Record

## HTTP POST - Create Record

## HTTP PUT/PATCH - Update Record

## HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(port=8000, debug=True)
