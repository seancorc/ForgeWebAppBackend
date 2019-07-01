import json
from flask import Flask, request
from db import db, Meal


app = Flask(__name__)

db_filename = 'todo.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % db_filename
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/')
def Hell():
    return "links for requests: \n To get all meals: '/api/meals/' \n To post a meal: post body - {title : String} - '/api/meal' \n To get a specific meal by id: '/api/meal/{id}'"

@app.route('/meals/')
def getMeals():
    allMeals = Meal.query.all()
    res = [meal.serialize() for meal in allMeals]
    return json.dumps(res), 200

@app.route('/meal/', methods=["POST"])
def createMeal():
    meal = json.loads(request.data)
    title = meal['title']
    data = Meal(title = title)
    db.session.add(data)
    db.session.commit()
    res = data.serialize()
    return json.dumps(res), 201

@app.route('/meal/<int:meal_id>/', methods=["POST"])
def checkMeal(meal_id):
    meal = Meal.query.filter_by(id=meal_id).first()
    if meal is None:
        return (json.dumps({'success': False, 'data': 'Not valid ID'})), 404
    meal.completed = (not meal.completed)
    db.session.commit()
    return json.dumps({'success': True, 'data': meal.serialize()}), 200

@app.route('/meal/<int:meal_id>/', methods=["DELETE"])
def deleteMeal(meal_id):
    meal = Meal.query.filter_by(id=meal_id).first()
    if meal is None:
        return (json.dumps({'success': False, 'data': 'Not valid ID'})), 404
    db.session.delete(meal)
    db.session.commit()
    return json.dumps({'success': True, 'data': meal.serialize()}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)