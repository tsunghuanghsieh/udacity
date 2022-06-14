from crypt import methods
import json
from flask import Flask, jsonify, request, abort
from models import setup_db, Plant
from flask_cors import CORS, cross_origin

PLANT_PER_PAGE = 10

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    setup_db(app)
    CORS(app)
    # CORS(app, resources={r"*/api/*" : {origins: '*'}})

    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        response.headers.add("Access-Control-Allow-Methods", "GET, POST, PATCH, DELETE, OPTION")
        return response

    @app.route('/plants')
    def get_plants():
        plants = Plant.query.order_by('id').all()
        formatted_plants = [plant.format() for plant in plants]

        page = request.args.get('page', 0, type = int)
        if (page < 1):
            # no pagination
            start = 0
            end = len(formatted_plants)
        else:
            # pagination
            start = (page - 1) * PLANT_PER_PAGE
            end = start + PLANT_PER_PAGE

        return jsonify({
            'success': True,
            'plants': formatted_plants[start:end],
            'total_plants': len(plants)
        })

    @app.route('/plants', methods=['POST'])
    def add_plant():
        name = request.form['name']
        scientific_name = request.form['scientific_name']
        is_poisonous = bool(request.form['is_poisonous'])
        primary_color = request.form['primary_color']
        plant = Plant(name, scientific_name, is_poisonous, primary_color)
        plant.insert()
        plant.update()
        return jsonify({
            'success': True,
            'plants': plant.format()
        })

    @app.route('/plants/<int:plant_id>')
    def get_plant(plant_id):
        plant = Plant.query.get(plant_id)
        if plant == None:
            abort(404)

        return jsonify({
            'success': True,
            'plants': plant.format()
        })

    @app.route('/plants/<int:plant_id>', methods = ['DELETE'])
    def delete_plant(plant_id):
        plant = Plant.query.get(plant_id)
        if plant == None:
            abort(404)

        plant.delete()

        return jsonify({
            'success': True,
        })

    return app