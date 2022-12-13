"""Flask app for Cupcakes"""

from flask import Flask, redirect, render_template, flash, get_flashed_messages, jsonify, request

from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"

DEFAULT_IMAGE_URL = "https://tinyurl.com/demo-cupcake"

# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

@app.get("/")
def cupcakes():

    return render_template("cupcakes.html")

@app.get("/api/cupcakes")
def get_all_cupcakes():
    """Get data about all cupcakes.
       Return JSON {'cupcakes': [{id, flavor, size, rating, image}, ...]}
    """


    cupcakes = Cupcake.query.all()
    serialized = [c.serialize() for c in cupcakes]

    return jsonify(cupcakes=serialized)

@app.get("/api/cupcakes/<cupcake_id>")
def get_cupcake(cupcake_id):
    """Get data about single cupcake
       Return JSON {'cupcake': {id, flavor, size, rating, image}}
    """


    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized = cupcake.serialize()

    return jsonify(cupcake=serialized)

@app.post("/api/cupcakes")
def create_cupcake():
    """
    Create a cupcake with flavor, size, rating and image data
    from the body of the request.
    Return JSON {'cupcake': [{id, flavor, size, rating, image}}
    """


    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image = request.json["image"] or None

    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)

    db.session.add(new_cupcake)
    db.session.commit()

    serialized = new_cupcake.serialize()

    return (jsonify(cupcake=serialized), 201)

@app.patch("/api/cupcakes/<cupcake_id>")
def update_cupcake(cupcake_id):
    """Update cupcake using the id passed in the URL and cupcake data passed
       in the body of the request.
       Respond with JSON {cupcake: {id, flavor, size, rating, image}}
    """

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    flavor = request.json.get("flavor", cupcake.flavor)
    size = request.json.get("size", cupcake.size)
    rating = request.json.get("rating", cupcake.rating)
    image = request.json.get("image", cupcake.image)

    cupcake.flavor = flavor
    cupcake.size = size
    cupcake.rating = rating
    cupcake.image = image


    db.session.commit()

    serialized = cupcake.serialize()

    return (jsonify(cupcake=serialized), 200)


@app.route("/api/cupcakes/<cupcake_id>", methods=["DELETE"])
def delete_cupcake(cupcake_id):
    """Delete cupcake. Respond with JSON like: {deleted: [cupcake-id]}"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)

    db.session.commit()


    return (jsonify(deleted = cupcake_id), 200)




