import os
from flask import Flask, request, abort, jsonify, render_template
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
#import random

from models import db, setup_db, Cases, Vaccination
from auth.auth import AuthError, requires_auth


# reference:  Exercise 4 - TDD for APIs
# https://github.com/udacity/cd0037-API-Development-and-Documentation-exercises/blob/master/4_TDD_Review/backend/flaskr/__init__.py
# from sqlalchemy.sql import func
#

def create_app(test_config=None):
    # create & configure the app
    app = Flask(__name__, template_folder='templates')
    setup_db(app)

    '''
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    '''
    CORS(app, resources={'/': {'origins': '*'}})

    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response


    @app.route('/', methods=['GET'])
    def index():
        return render_template('index.html') #"Here is some information about Covid situation in Sweden."

    @app.route('/cases', methods=['GET'])
    #@requires_auth('get:cases')
    def fetch_cases(): #
        # get all cases
        cases = Cases.query.order_by(Cases.age_group).all()
        # categories_dict = {}
        # for category in categories:
        # categories_dict[category.id] = category.type
        cases_info = [case.format() for case in cases]

        # abort 404 if no categories
        if (len(cases_info) == 0):
            abort(404)

        # return data to view
        return jsonify({
            'success': True,
            'cases_info': cases_info
        })


    @app.route('/cases/<string:agegroup>', methods=['GET'])
    #@requires_auth('get:case_agegroup')
    def fetch_cases_agegroup(agegroup):

        # get all cases
        cases = Cases.query.filter(Cases.age_group == agegroup).one_or_none()
        if not cases:
            return jsonify({
                'success': False,
                'error': 400,
                'message': 'Please provide correct age group!'
            })

        return jsonify({
            'success': True,
            'case_info': cases.format()
        })

    @app.route('/cases', methods=['POST'])
    @requires_auth('post:cases')
    def create_cases(token):
        body = request.get_json()
        age_group = body.get('age_group', None)
        total_num_case = body.get('total_num_case', None)
        total_num_intensivecare = body.get('total_num_intensivecare', None)
        total_num_death = body.get('total_num_death', None)

        if not age_group or not total_num_case or not total_num_intensivecare or not total_num_death:
            return jsonify({
                'success': False,
                'error': 400,
                'message': 'Information is missing!'
            })

        try:
            case = Cases(age_group=age_group,
                         total_num_case=total_num_case,
                         total_num_intensivecare=total_num_intensivecare,
                         total_num_death=total_num_death)
            case.insert()

            new_case = Cases.query.get(case.age_group).format()

            return jsonify({
                'success': True,
                'case_age_group': case.age_group,
                'new case': new_case
            })

        except Exception:
            abort(422)


    @app.route('/cases/<string:agegroup>', methods=['PATCH'])
    @requires_auth('patch:cases')
    def update_cases(token, agegroup):
        body = request.get_json()
        age_group = body.get('age_group', None)
        total_num_case = body.get('total_num_case', None)
        total_num_intensivecare = body.get('total_num_intensivecare', None)
        total_num_death = body.get('total_num_death', None)

        case = Cases.query.filter(Cases.age_group == agegroup).one_or_none()
        if not case:
            return jsonify({
                'success': False,
                'error': 400,
                'message': 'Please provide correct age group!'
            })

        try:
            if age_group:
                case.age_group = age_group
            if total_num_case:
                case.total_num_case = total_num_case
            if total_num_intensivecare:
                case.total_num_intensivecare = total_num_intensivecare
            if total_num_death:
                case.total_num_death = total_num_death

            case.update()
            
            return jsonify({
            'success': True,
            'case': case.format()
        })

        except Exception:
            abort(422)

    
    @app.route('/cases/<string:agegroup>', methods=['DELETE'])
    @requires_auth('delete:cases')
    def delete_case(token, agegroup):
        try:
            # get the case by its agegroup
            case = Cases.query.filter(Cases.age_group==agegroup).one_or_none()

            # abort if no cases found
            if case is None:
                abort(404)

            case.delete()

            return jsonify({
            'success': True,
            'deleted_age_group': agegroup
                })

        except:
            # abort if problem of deleting cases
            abort(422)


    # Vaccination
    @app.route('/vaccinations', methods=['GET'])
    #@requires_auth('get:vaccin')
    def fetch_top10_vaccinations(): 
        # get top 10 fully vaccinated age group & region
        vaccin = db.session.query(Vaccination.age_group, Vaccination.region, func.sum(Vaccination.num_fully_vaccinated).label('total_number_of_fully_vaccinated')).group_by(Vaccination.age_group, Vaccination.region).order_by(func.sum(Vaccination.num_fully_vaccinated).desc()).limit(10).all()

        # [vac.format().get('region') for vac in vaccin]
        # abort for bad request if no vaccin info
        if vaccin is None:
            abort(400)

        return jsonify({
            'success': True,
            'top 10 fully vaccinated groups': {i+1:row._asdict() for i, row in enumerate(vaccin)}
            })


    @app.route('/vaccinations/<int:vacc_id>', methods=['GET'])
    #@requires_auth('get:vaccin')
    def fetch_vaccinations_by_id(vacc_id): # token,
        # get the vacc by id
        vaccin = Vaccination.query.filter(Vaccination.id==vacc_id).one_or_none()

        # abort for bad request if no vaccin info
        if vaccin is None:
            abort(400)

        return jsonify({
            'success': True,
            'vaccination_info': vaccin.format()
            })


    @app.route('/vaccinations', methods=['POST'])
    #@requires_auth('post:vaccin')
    def create_vaccin():
        body = request.get_json()
        #print(body)
        id = body.get('vaccination_info_id', None)
        region = body.get('region', None)
        kommun_namn = body.get('kommun_namn', None)
        age_group = body.get('age_group', None)
        population = body.get('population', None)
        num_minst_1_dos = body.get('num_minst_1_dos', None)
        num_fully_vaccinated = body.get('num_fully_vaccinated', None)
        proportion_of_minst_1_dos = body.get('proportion_of_minst_1_dos', None)
        proportion_of_fully_vaccinated = body.get('proportion_of_fully_vaccinated', None)

        if not id or not region or not kommun_namn or not age_group or not population or not num_minst_1_dos or not num_fully_vaccinated or not proportion_of_minst_1_dos or not proportion_of_fully_vaccinated:
            return jsonify({
                'success': False,
                'error': 400,
                'message': 'Information is missing.'
                })

        try:
            vaccin = Vaccination(id=id, region=region, kommun_namn=kommun_namn, age_group=age_group, population=population,
                             num_minst_1_dos=num_minst_1_dos, num_fully_vaccinated=num_fully_vaccinated,
                             proportion_of_minst_1_dos=proportion_of_minst_1_dos,
                             proportion_of_fully_vaccinated=proportion_of_fully_vaccinated)
            vaccin.insert()
            print(vaccin)
            vacc_format = Vaccination.query.get(vaccin.id).format()
        #print(vacc_format)
            return jsonify({
                'success': True,
                'age_group': vaccin.age_group,
                'new_vaccination': vacc_format
               })

        except Exception:
            abort(422)


    @app.route('/vaccinations/<int:vacc_id>', methods=['DELETE'])
   # @requires_auth('delete:vaccin')
    def delete_vaccin(vacc_id):
        #https://www.py4u.net/discuss/149022
        vaccin = db.session.query(Vaccination).filter(Vaccination.id == vacc_id)
        #vaccin = Vaccination.query.filter(Vaccination.id == vacc_id).one_or_none()
        if not vaccin:
            return jsonify({
                'success': False,
                'error': 400,
                'message': 'Vaccination Id is not correct.'
                })
        #print(vaccin)
        try:
            vaccin.delete(synchronize_session=False)
            return jsonify({
                'success': True,
                'deleted': vacc_id
                })

        except Exception:
            abort(422)


    '''
    @TODO: 
    Create error handlers for all expected errors  
    '''

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request!"
            })


    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource not found!"
        }), 404


    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable!"
        }), 422


    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            'success': False,
            'message': 'Internal server error!',
            'error': 500
        }), 500

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)  # host='0.0.0.0', port=8080, 


