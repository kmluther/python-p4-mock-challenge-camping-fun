#!/usr/bin/env python3

from flask import Flask, make_response, request
from flask_migrate import Migrate

from models import db, Camper, Signup, Activity

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return ''

@app.route('/campers', methods=['GET', 'POST'])
def campers():
    if request.method == 'GET':
        return make_response([camper.to_dict() for camper in Camper.query.all()], 200)
    elif request.method == 'POST':
        new_camper = Camper(
            name = request.get_json()['name'],
            age = request.get_json()['age']
        )
        db.session.add(new_camper)
        db.session.commit()
        try:
            return make_response(new_camper.to_dict(), 201)
        except ValueError:
            return make_response({'error': '400: Validation error'}, 400)

@app.route('/campers/<int:id>')
def campers_by_id(id):
    camper = Camper.query.filter_by(id=id).first()

    if not camper:
        return make_response({'error': '404: Camper not found'}, 404)
    return make_response(camper.to_dict(), 200)
            
@app.route('/activities')
def activities():
    return make_response([activity.to_dict() for activity in Activity.query.all()], 200)

@app.route('/activities/<int:id>', methods=['DELETE'])
def activity_by_id(id):
    activity = Activity.query.filter_by(id=id).first()
    if not activity:
        return make_response({'error': '404: Activity not found'}, 404)
    elif request.method == 'DELETE':
        db.session.delete(activity.signups)
        db.session.delete(activity)
        db.session.commit()
        return make_response({}, 204)

@app.route('/signups', methods=['POST'])
def signups():
    new_signup = Signup(
        time = request.get_json()['time'],
        camper_id = request.get_json()['camper_id'],
        activity_id = request.get_json()['activity_id']
    )
    db.session.add(new_signup)
    db.session.commit()

    try:
        return make_response(new_signup.activity.to_dict(), 201)
    except ValueError:
        return make_response({'error': '400: Validation error'}, 400)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
