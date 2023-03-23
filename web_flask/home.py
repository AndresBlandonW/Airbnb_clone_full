#!/usr/bin/python3
""" Starts a Flash Web Application """
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from os import environ
from flask import Flask, jsonify, render_template, redirect, request
app = Flask(__name__)
# app.jinja_env.trim_blocks = True
# app.jinja_env.lstrip_blocks = True


@app.teardown_appcontext
def close_db(error):
    """ Remove the current SQLAlchemy Session """
    storage.close()


@app.template_filter('getuser')
def getuser_filter(uid):
    user = storage.get("User", uid)
    return user.first_name + " " + user.last_name


@app.route('/', methods = ['POST', 'GET'], strict_slashes=False)
def hbnb():
    """ HBNB home screen! """

    # GET VALUES OF STORAGE
    amenities = storage.all("Amenity").values()
    places = storage.all("Place").values()
    users = storage.all("User").values()
    states = storage.all("State").values()
    
    st_ct = []
    cities = ""

    # ADD NAME OWNERS TO PLACE
    for place in places:
        for user in users:
            if place.user_id == user.id:
                setattr(place, "owner", user.first_name + " " + user.last_name)
    

    # IF SEARCH BUTTON
    if request.method == "POST":
        am_list = request.form.getlist('amenity')
        print(am_list)
        city_id = request.form['city']
        places = storage.all("Place").values()
        res_places = []
        
        
        for place in places:
            #
            placeam = []
            for amobj in place.amenities:
                placeam.append(amobj.id)

            if place.city_id == city_id:
                check = all(item in placeam for item in am_list)
                print(check)
                if check:
                    res_places.append(place)


        cities = storage.get("City", city_id)
        places = sorted(res_places, key=lambda k: k.name)
    else:
        places = sorted(places, key=lambda k: k.name)
    
    # SORT RESULTS
    states = sorted(states, key=lambda k: k.name)
    for state in states:
        st_ct.append([state, sorted(state.cities, key=lambda k: k.name)])
    amenities = sorted(amenities, key=lambda k: k.name)

    return render_template('index.html', city=cities, states=st_ct, amenities=amenities, places=places)


@app.route('/place/<place_id>', methods = ['POST', 'GET'], strict_slashes=False)
def place(place_id):
    place = storage.get("Place", place_id)
    users = storage.all("User").values()

    # ADD NAME OWNERS TO PLACE
    for user in users:
        if place.user_id == user.id:
            setattr(place, "owner", user.first_name + " " + user.last_name)
    
    return render_template('place.html', place=place)


if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5000)
