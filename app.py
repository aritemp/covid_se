from flask import Flask, request, abort, jsonify, render_template, redirect, session, url_for
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import urlencode
from flask_cors import CORS, cross_origin

#import random

from models import db, setup_db, Cases, Vaccination  #, CaseForm, VaccinForm
from auth.auth import *

from functools import wraps
import json
import os
#from os import environ as env
from werkzeug.exceptions import HTTPException
#from dotenv import load_dotenv, find_dotenv
from authlib.integrations.flask_client import OAuth
from six.moves.urllib.parse import urlencode


#ENV_FILE = find_dotenv()
#if ENV_FILE:
#load_dotenv()

AUTH0_DOMAIN = 'fwddev.eu.auth0.com' #os.environ.get('AUTH0_DOMAIN')
CLIENT_ID = '9P90EvszrUfHRmp2AKTOiQsYUIbykQIn'  #os.environ['CLIENT_ID']
JWT_SECRET_KEY = 'U1wxAOAfTEyU1D-N-gyMgbs4cVXiUAeRBbAGfcG61a4glJaKSBuBvERBFcp4CFsT'  #os.environ.get('JWT_SECRET_KEY')
API_AUDIENCE = 'se_covid2021' #os.environ.get('API_AUDIENCE')
AUTH0_CALLBACK_URL = 'http://0.0.0.0:8080' #os.environ.get('AUTH0_CALLBACK_URL')
AUTH0_BASE_URL = 'https://' + AUTH0_DOMAIN

# reference:  Exercise 4 - TDD for APIs
# https://github.com/udacity/cd0037-API-Development-and-Documentation-exercises/blob/master/4_TDD_Review/backend/flaskr/__init__.py
# from sqlalchemy.sql import func
#

def create_app(test_config=None):
    # create & configure the app
    app = Flask(__name__, template_folder='templates') #
    setup_db(app)

    '''
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    '''
    CORS(app, resources={'/': {'origins': '*'}})
    app.secret_key = JWT_SECRET_KEY # env.get("JWT_SECRET_KEY")

    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''
    #"""
    # OAUTH 

    oauth = OAuth(app)

    auth0 = oauth.register(
        'auth0',
        client_id=CLIENT_ID,
        client_secret=JWT_SECRET_KEY,
        api_base_url=AUTH0_BASE_URL,
        access_token_url=AUTH0_BASE_URL + '/oauth/token',
        authorize_url=AUTH0_BASE_URL + '/authorize',
        client_kwargs={
        'scope': 'openid profile email',
        },)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

    # Configure login page
    @app.route("/", methods=['GET'])
    def index():
        if session.get("token"):
            return redirect("/callback")
        else:
            #print(session)
            return render_template("index.html", login=True)   # "Here is some information about Covid situation in Sweden."

    @app.route('/login')
    def login():
        return auth0.authorize_redirect(redirect_uri=AUTH0_CALLBACK_URL+ '/callback', audience=API_AUDIENCE)


    @app.route('/callback')
    def callback_handling():

        if session.get("token"):
            token = session["token"]
        else:
            acc_token = auth0.authorize_access_token()
            session['token'] = acc_token['access_token']
            token = acc_token['access_token']
        try:
            payload = verify_decode_jwt(token)

            permissions = payload["permissions"]
        except :
            abort(401)


        if permissions == [ "get:case_agegroup", "get:cases", "get:vaccin"]:
            return render_template('index.html', permissions=permissions, token=True)

        elif permissions == ["delete:cases", "delete:vaccin", "get:case_agegroup", "get:cases",
                                "get:vaccin", "patch:cases", "post:cases", "post:vaccin"]:
            print('Admin logged in.')
            return render_template('index.html', permissions=permissions, token=True)

        else:
            return render_template('index.html')

    
    @app.route('/logout')
    def logout():
        session.clear()
        params = {'returnTo': url_for('index', _external=True), 'client_id': CLIENT_ID}
        return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))


    @app.route('/cases', methods=['GET'])
    @cross_origin()
    @requires_auth('get:cases')
    def fetch_cases(payload): #
        permissions = payload["permissions"]
        # get all cases
        cases = Cases.query.order_by(Cases.age_group).all()
        # categories_dict = {}
        # for category in categories:
        # categories_dict[category.id] = category.type
        cases_info = [case.format() for case in cases]

        # abort 404 if no cases
        if (len(cases_info) == 0):
            abort(404)

        # return data to view
        return jsonify({
            'success': True,
            'cases_info': cases_info
        }), render_template("cases.html", cases=cases, permissions=permissions)


    @app.route('/cases/<string:agegroup>', methods=['GET'])
    @cross_origin()
    @requires_auth('get:case_agegroup')
    def fetch_cases_agegroup(payload, agegroup):

        # get all cases
        permissions = payload["permissions"]
        case = Cases.query.filter(Cases.age_group == agegroup).one_or_none()
        if not case:
            return jsonify({
                'success': False,
                'error': 400,
                'message': 'Please provide correct age group!'
            })

        return jsonify({
            'success': True,
            'cases_info': case.format()
        }), render_template("cases.html", case=case, permissions=permissions)


    @app.route('/cases', methods=['POST'])
    @cross_origin()
    @requires_auth('post:cases')
    def create_cases(payload):
        permissions = payload["permissions"]
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

            #return redirect(url_for("cases"))

            new_case = Cases.query.get(case.age_group).format()

            return jsonify({
                'success': True,
                'case_age_group': case.age_group,
                'new case': new_case
            }), render_template("cases.html", permissions=permissions, new_case=new_case)

        except Exception:
            abort(422)


    @app.route('/cases/<string:agegroup>', methods=['PATCH'])
    @cross_origin()
    @requires_auth('patch:cases')
    def update_cases(payload, agegroup):
        # modify case info by age group
        permissions = payload["permissions"]

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
                cases.total_num_death = total_num_death


            case.update()
            
            return jsonify({
            'success': True,
            'case': case.format()
        }), render_template("cases.html", permissions=permissions, update_case=case)

        # redirect(url_for("case_age_group", payload=payload, age_group = age_group))

        except Exception:
            abort(422)

    
    @app.route('/cases/<string:agegroup>', methods=['DELETE'])
    @cross_origin()
    @requires_auth('delete:cases')
    def delete_case(payload, agegroup):
        try:
            # get the case by its agegroup
            case = Cases.query.filter(Cases.age_group==agegroup).one_or_none()

            # abort if no cases found
            if case is None:
                abort(404)

            permissions = payload["permissions"]
            case.delete()

            return jsonify({
            'success': True,
            'deleted_age_group': agegroup
                }), render_template("cases.html", delete_case=agegroup, permissions=permissions)

        except:
            # abort if problem of deleting cases
            abort(422)


    # Vaccination
    @app.route('/vaccinations', methods=['GET'])
    @cross_origin()
    @requires_auth('get:vaccin')
    def fetch_top10_vaccinations(payload): #
        # get top 10 fully vaccinated age group & region

        permissions = payload["permissions"]
        vaccins = db.session.query(Vaccination.age_group, Vaccination.region, func.sum(Vaccination.num_fully_vaccinated).label('total_number_of_fully_vaccinated')).group_by(Vaccination.age_group, Vaccination.region).order_by(func.sum(Vaccination.num_fully_vaccinated).desc()).limit(10).all()

        # [vac.format().get('region') for vac in vaccin]
        # abort for bad request if no vaccin info
        if vaccins is None:
            abort(400)

        vaccins = {i+1:row._asdict() for i, row in enumerate(vaccins)}

        return jsonify({
            'success': True,
            'top 10 fully vaccinated groups': vaccins
            }), render_template("vaccinations.html", vaccins=vaccins, permissions=permissions)


    @app.route('/vaccinations/<int:vacc_id>', methods=['GET'])
    @cross_origin()
    @requires_auth('get:vaccin')
    def fetch_vaccinations_by_id(payload, vacc_id):

        permissions = payload["permissions"]
        # get the vacc by id
        vaccin = Vaccination.query.filter(Vaccination.id==vacc_id).one_or_none()

        # abort for bad request if no vaccin info
        if vaccin is None:
            abort(400)

        return jsonify({
            'success': True,
            'vaccination': vaccin.format()
            }), render_template("vaccinations.html", vaccin=vaccin, permissions=permissions)


    @app.route('/vaccinations', methods=['POST'])
    @cross_origin()
    @requires_auth('post:vaccin')
    def create_vaccin(payload):

        permissions = payload["permissions"]

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
            #print(vaccin)
            vacc_format = Vaccination.query.get(vaccin.id).format()
        #print(vacc_format)
            return jsonify({
                'success': True,
                'age_group': vaccin.age_group,
                'new_vaccination': vacc_format
               }), redirect(url_for("vaccinations")), render_template("vaccinations.html",
                                                                      permissions=permissions, new_vaccin=vaccin)

        except Exception:
            abort(422)


    @app.route('/vaccinations/<int:vacc_id>', methods=['DELETE'])
    @cross_origin()
    @requires_auth('delete:vaccin')
    def delete_vaccin(payload, vacc_id):

        vaccin = Vaccination.query.filter(Vaccination.id == vacc_id).one_or_none()
        if not vaccin:
            return jsonify({
                'success': False,
                'error': 400,
                'message': 'Vaccination Id is not correct.'
                })

        permissions = payload["permissions"]
        vaccin.delete()
        return jsonify({
                'success': True,
                'deleted': vacc_id
                }), render_template("vaccinations.html", permissions=permissions, delete_vaccin=vacc_id)

        #except Exception:
            #abort(422)


    '''
    @TODO: 
    Create error handlers for all expected errors  
    '''

    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response

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
    app.run(host='0.0.0.0', port=8080, debug=True) 
