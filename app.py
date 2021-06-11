"""Flask app for Cupcakes"""
from flask import Flask, render_template, redirect, flash, jsonify, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = "hush"
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/api/cupcakes')
def api_get_all_cupcakes():
    cupcakes = Cupcake.query.all()
    output = {"cupcakes": [cupcake.serialize_cupcake()
                           for cupcake in cupcakes]}
    return jsonify(output)


@app.route('/api/cupcakes/<cupcake_id>')
def api_get_one_cupcake(cupcake_id):
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify({"cupcake": cupcake.serialize_cupcake()})


@app.route('/api/cupcakes', methods=['POST'])
def add_cupcake():
    """Accepts info for new cupcake and creates the object"""
    flavor = request.json["flavor"] if request.json['flavor'] else None
    size = request.json['size'] if request.json['size'] else None
    rating = request.json['rating'] if request.json['rating'] else None
    image = request.json['image'] if request.json['image'] else None

    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)

    db.session.add(new_cupcake)
    db.session.commit()

    return (jsonify({"cupcake": new_cupcake.serialize_cupcake()}), 201)


@app.route('/api/cupcakes/<cupcake_id>', methods=['PATCH'])
def update_cupcake(cupcake_id):
    """Update Cupcake object"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    cupcake.flavor = request.json["flavor"]
    cupcake.size = request.json['size']
    cupcake.rating = request.json['rating']
    cupcake.image = request.json['image']
    db.session.commit()

    return (jsonify({"cupcake": cupcake.serialize_cupcake()}))


@app.route('/api/cupcakes/<cupcake_id>', methods=['DELETE'])
def delete_cupcake(cupcake_id):
    """Delete cupcake"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    return (jsonify({"deleted": cupcake.id}))


@app.route('/')
def home():
    return render_template('home.html')
