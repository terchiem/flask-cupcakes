"""Flask app for Cupcakes"""

from flask import Flask, jsonify, request, render_template
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()


# TODO: status code constants

def serialize_cupcake(cupcake):
    """ Serialize class into a dictionary """

    return {
        "id": cupcake.id,
        "flavor": cupcake.flavor,
        "size": cupcake.size,
        "rating": cupcake.rating,
        "image": cupcake.image
    }


@app.route('/api/cupcakes')
def get_cupcake_list():
    """ Get a list of all cupcakes """

    cupcakes = Cupcake.query.all()

    serialized = [ serialize_cupcake(c) for c in cupcakes ]

    return ( jsonify(cupcakes=serialized), 200 )


@app.route('/api/cupcakes/<int:cupcake_id>')
def get_cupcake(cupcake_id):
    """ Get data about a single cupcake """

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    # TODO: check the cupcake, handle if 404

    serialized = serialize_cupcake(cupcake)

    return ( jsonify(cupcake=serialized), 200 )


@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    """ Create a cupcake """

    flavor = request.json['flavor']
    size = request.json['size']
    rating = float(request.json['rating'])
    image = request.json['image'] or None
    # TODO: check for key error

    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)

    db.session.add(new_cupcake)
    db.session.commit()

    serialized = serialize_cupcake(new_cupcake)

    return ( jsonify(cupcake=serialized), 201 )

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def update_cupcake(cupcake_id):
    """ Update the cupcake"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = request.json['flavor']
    cupcake.size = request.json['size']
    cupcake.rating = float(request.json['rating'])
    cupcake.image = request.json['image'] or None
    # TODO: check for key error

    db.session.commit()

    serialized = serialize_cupcake(cupcake)

    return (jsonify(cupcake=serialized), 200)


@app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
def delete_cupcake(cupcake_id):
    """ Delete the cupcake"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return (jsonify( { "message": "Deleted"}), 200)


@app.route('/api/search')
def search_cupcakes():
    """ Search for a cupcake """

    search_flavor = request.args['flavor']

    # query db with data
    cupcakes = Cupcake.query.filter(Cupcake.flavor == search_flavor).all()

    # return json of results
    serialized = [ serialize_cupcake(c) for c in cupcakes ]

    return ( jsonify(cupcakes=serialized), 200 )


###############
# Form routes

@app.route('/')
def cupcake_form():
    """ Return static html for cupcake entry """

    return render_template('cupcake_form.html')

@app.route('/search')
def cupcake_search_form():
    """ Return static html for cupcake search """

    return render_template('cupcake_search.html')
