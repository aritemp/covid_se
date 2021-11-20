import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import db, setup_db, Cases, Vaccination


class CovidSETestCase(unittest.TestCase):
    """This class represents the covid se test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.DB_HOST = os.getenv('DB_HOST', 'localhost:5432')
        self.DB_USER = os.getenv('DB_USER', 'postgres')
        self.DB_PASSWORD = os.getenv('DB_PASSWORD', 'fwd2021')
        self.DB_NAME = os.getenv('DB_NAME', 'covid')
        self.database_path = "postgresql://{}:{}@{}/{}".format(self.DB_USER, self.DB_PASSWORD, self.DB_HOST, self.DB_NAME)
        setup_db(self.app, self.database_path)
        
        self.admin= os.getenv('ADMIN')
        self.user = os.getenv('USER')

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    #def tearDown(self):
        """Executed after reach test"""
       # pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_all_cases(self):
        res = self.client().get('/cases' ,
            headers={
                "Authorization": "Bearer {}".format(
                    self.user)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['cases_info'])

    def test_404_no_valid_cases(self):

        # get the request with invalid page
        res = self.client().get('/cases',
            headers={
                "Authorization": "Bearer {}".format(
                    self.user)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found!')

    def test_create_cases(self):
        
        new_cases = {
            "age_group": "18-29",  # fake data
            "total_num_case": 273093,
            "total_num_death": 12,
            "total_num_intensivecare": 200
        }

        res = self.client().post('/cases', json=new_cases, headers={
                "Authorization": "Bearer {}".format(
                    self.admin)})
        data = json.loads(res.data)
        # check if the case has been created or not 
        case = Cases.query.filter_by(age_group=data['case_age_group']).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(case)

    def test_update_case(self):
        # update a case group
        response = self.client().patch(
            '/cases/18-29',
            json={
               "age_group": "18-29", 
                "total_num_case": 25000, 
                "total_num_death": 12, 
                "total_num_intensivecare": 200
                },
            headers={
                "Authorization": "Bearer {}".format(
                    self.admin)})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['case'])
                                
    def test_400_update_case(self):
                                
        response = self.client().patch(
            '/cases/18-25',
            json={
               "age_group": "18-25", 
                "total_num_case": 25000, 
                "total_num_death": 12,
               "total_num_intensivecare": 200
                },
            headers={
                "Authorization": "Bearer {}".format(
                    self.admin)})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Please provide correct age group!')

    def test_create_vaccin(self):
        
        new_cases = { "age_group":"80-89",
            "kommun_namn":"TEST_Vallentuna",
            "num_fully_vaccinated":1545,
            "num_minst_1_dos":1095,
            "population":1243,
            "proportion_of_fully_vaccinated":0.9070290390000001,
            "proportion_of_minst_1_dos":0.9780290390000001,
            "region":"Stockholm",
            "vaccination_info_id":10 }
        
        res = self.client().post('/vaccinations', json=new_cases, headers={
                "Authorization": "Bearer {}".format(
                    self.admin)})
        data = json.loads(res.data)
        # check if the vaccin info has been created or not 
        vaccin = Vaccination.query.filter_by(id=data['vaccination_info_id']).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(vaccin)
        
    def test_400_vaccin_creation_failure(self):

        # create a new vaccin
        res = self.client().post('/vaccinations', json={}, headers={
                "Authorization": "Bearer {}".format(
                    self.admin)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad request!')

    def test_fetch_top10_vaccin(self):

        res = self.client().get('/vaccinations', json={}, headers={
                "Authorization": "Bearer {}".format(
                    self.admin)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_400_fetch_top10_vaccin(self):

        res = self.client().get('/vaccinations/', json={}, headers={
                "Authorization": "Bearer {}".format(
                    self.user)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad request!')

    def test_fetch_vaccin_by_id(self):

        res = self.client().get('/vaccinations/11', json={}, headers={
                "Authorization": "Bearer {}".format(
                    self.admin)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_400_fetch_vaccin(self):

        res = self.client().get('/vaccinations/1', json={}, headers={
                "Authorization": "Bearer {}".format(
                    self.user)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad request!')

    def test_delete_vaccin(self):
        
        res = self.client().delete('/vaccinations/10', json={}, headers={
                "Authorization": "Bearer {}".format(
                    self.admin)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_vaccination_info_id'], 10)
        

    def test_404_delete_vaccin(self):
        
        res = self.client().delete('/vaccinations/5005', json={}, headers={
                "Authorization": "Bearer {}".format(
                    self.admin)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Resource not found!")

    def test_422_fetch_vaccin(self):
         
        res = self.client().post('/vaccinations', json={
            'vaccination_info_id':5000,
            'region': 'Skoone',
            'kommun_namn': 'Äöge',   # fake data
            'age_group': '10-15',
            'population': 56666,
            'num_minst_1_dos': 6278,
            'num_fully_vaccinated': 9000,
            'proportion_of_minst_1_dos': 0.1108,
            'proportion_of_fully_vaccinated': 0.1588
            }, headers={
                "Authorization": "Bearer {}".format(
                    self.admin)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)



if __name__ == "__main__":
    unittest.main()
    #app.run(host='0.0.0.0')
