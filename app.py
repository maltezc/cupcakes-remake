"""Flask app for Cupcakes"""

from flask import Flask, render_template, redirect, jsonify, request

from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///adopt"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:
#
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)


#####################################RENDER ROUTES#######################
@app.get('/')
def render_homepage():
    """Renders the homepage"""

    # TODO: confirm that you dont need to look in the templates folder ex: `render_template("/templates/index.html")`
    return render_template("index.html")

#####################################API ROUTES#######################
@app.get('/api/cupcakes')
def get_all_cupcakes():
    """Retreives all cupcakes"""

    # query all
    cupcakes = Cupcake.query.all()

    # serialize all with list comprehension
    serialized = [cupcake.serialize() for cupcake in cupcakes]

    #return as jsonify
    return jsonify(cupcakes=serialized)

@app.get('/api/cupcakes/<int:cupcake_id>')
def get_single_cupcake(cupcake_id):
    """Retreives a single cupcake"""

    #query cupcake
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    #serialize cupcake
    serialized = cupcake.serialize()

    #return as jsonify
    return jsonify(cupcake=serialized) #returns as json string

@app.post('/api/cupcakes')
def create_cupcake():
    """Creates a cupcake"""

    flavor = request.json['flavor']
    size = request.json['size']
    rating = request.json['rating']
    image = request.json['image'] or None

    # creates a new instance of cupcake. property_from_model=form_input_value
    new_cupcake = Cupcake(
        flavor=flavor,
        size=size,
        rating=rating,
        image=image
        )

    db.session.add(new_cupcake)
    db.session.commit()

    serialized = new_cupcake.serialize()

    # TODO: what determines "cupcake" in line below?
    return (jsonify(cupcake=serialized), 201)


@app.patch('/api/cupcakes/<int:cupcake_id>')
def update_cupcake(cupcake_id):
    """Updates cupcake information"""

    # get existing cupcake value or 404
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    # get value if new info
    #pull property = request.json.get(newValue, or return existing db value)
    cupcake.flavor = request.json.get("flavor", cupcake.flavor)
    cupcake.size = request.json.get("size", cupcake.size)
    cupcake.rating = request.json.get("rating", cupcake.rating)
    cupcake.image = request.json.get("image", cupcake.image)

    #serialize
    serialized = cupcake.serialize()

    #commit
    db.session.commit() # TODO: IS THIS LINE NOT NECESSARY? DIDNT HAVE IN ORIGINAL

    #return jsonify
    return (jsonify(cupcake=serialized), 200)


@app.delete('/api/cupcakes/<int:cupcake_id>')
def delete_cupcake(cupcake_id):
    """Deletes a specified cupcake"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return (jsonify(deleted=cupcake_id), 200)
