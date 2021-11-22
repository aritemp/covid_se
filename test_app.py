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
        #"""
        self.DB_HOST = os.getenv('DB_HOST', 'localhost:5432')
        self.DB_USER = os.getenv('DB_USER', 'postgres')
        self.DB_PASSWORD = os.getenv('DB_PASSWORD', 'fwd2021')
        self.DB_NAME = os.getenv('DB_NAME', 'covid')
        self.database_path = "postgresql://{}:{}@{}/{}".format(self.DB_USER, self.DB_PASSWORD, self.DB_HOST, self.DB_NAME)
        #"""
        #self.database_path = 'postgresql://qrjpxglmlwfvmj:0704636590cebfd1a6fe3b8942bf8d8c936a8bd5e12bd3765f3a6c88af9fb604@ec2-23-23-133-10.compute-1.amazonaws.com:5432/dcup748f1vqo46'
        setup_db(self.app, self.database_path)
        
        self.admin= 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im9mU0poLW1tSm1EczNpcFBiRW9KQyJ9.eyJpc3MiOiJodHRwczovL2Z3ZGRldi5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjE5MGQ4NGZhM2EzODYwMDZhYjVlNzY5IiwiYXVkIjpbInNlX2NvdmlkMjAyMSIsImh0dHBzOi8vZndkZGV2LmV1LmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2Mzc1MzM0ODMsImV4cCI6MTYzNzYxOTg4MywiYXpwIjoiOVA5MEV2c3pyVWZIUm1wMkFLVE9pUXNZVUlieWtRSW4iLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmNhc2VzIiwiZGVsZXRlOnZhY2NpbiIsImdldDpjYXNlX2FnZWdyb3VwIiwiZ2V0OmNhc2VzIiwiZ2V0OnZhY2NpbiIsInBhdGNoOmNhc2VzIiwicG9zdDpjYXNlcyIsInBvc3Q6dmFjY2luIl19.OjB7797bFbSUt3z83LDSRXlLMpvZeZfB6MDDEnsfEbQ6EWF_hO8BHE3xVx9z8h9KFOQe5GoEyX4bDQlsdH0vtQN76IMIqhFDgjWDeq0iSQd6tv8rFPSX2wGL_8y97GjiLc6gcAq7CLx1VYVjpB_gVb187gz4Rs2B7QSX7x_zS1eaA4O0UXNBRxh9Afbv4fKa5MxLpgWBRVkn7jxeXz1ikj4mtvALlkIWfRLwCSglY74Yjcn_gCnmGzwOEkK_iHAH64bH8JNgPyODI4v75D3F2cago7hc9uDDrMc3FQoxz6VjXlDdNP-OWiRHoTf_fFBCaoQGx9g1KRQkqa6rDC-B5A'

        self.user = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im9mU0poLW1tSm1EczNpcFBiRW9KQyJ9.eyJpc3MiOiJodHRwczovL2Z3ZGRldi5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjE5MGQ3Y2Y0NzBkMDcwMDY5MzA5MDA4IiwiYXVkIjpbInNlX2NvdmlkMjAyMSIsImh0dHBzOi8vZndkZGV2LmV1LmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2Mzc1NzkxMzEsImV4cCI6MTYzNzY2NTUzMSwiYXpwIjoiOVA5MEV2c3pyVWZIUm1wMkFLVE9pUXNZVUlieWtRSW4iLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZ2V0OmNhc2VfYWdlZ3JvdXAiLCJnZXQ6Y2FzZXMiLCJnZXQ6dmFjY2luIl19.CNUg-2ZSgCZJFz8l9c0DB3qRmdxseGfk_LFWXf6GHnT2zRIMhcjH-fp4xmDUpYYBf7SZt-8qb6LT4tX7n7VCqL1-jKINS1MsGtvKTEXCeymxTL--ClHNizQTeMiI17R1BnENweLn-pZg5ffkMsbBVsIf_aHtVRYzb8DsFeMqsNK2V7pr7pzMQfWawLQjK4jvMd1g6h8yE1JCXREqvINYkmWvQkiI5BXDsNCICRgLUJ8mAwoNI5stMFz3H0leFPY_YTRBztEpeCIqGSE1-5EMUJlae3k044TeBxg_9yJh04BCrM3Xy7Y5ce5oizHXGi6KJkKI_FlXpdKxcsX2ZLxTIA'

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
    # Cases
    def test_get_all_cases(self):
        res = self.client().get('/cases', headers={"Authorization": "Bearer {}".format(self.user)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['cases_info'])

    def test_404_no_valid_cases(self):

        # get the request with invalid page
        res = self.client().get('/cases/', headers={"Authorization": "Bearer {}".format(self.user)})
        data = json.loads(res.data)
        #print(data)
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

        res = self.client().post('/cases', json=new_cases, headers={"Authorization": "Bearer {}".format(self.admin)})
        data = json.loads(res.data)
        # check if the case has been created or not
        case = Cases.query.filter_by(age_group=new_cases['age_group']).one_or_none()
        #print(case)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(case)

    def test_400_create_cases(self):

        # get the request with invalid page
        res = self.client().get('/cases', json={}, headers={"Authorization": "Bearer {}".format(self.admin)})
        data = json.loads(res.data)
        #print(data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Information is missing!')

    def test_update_case(self):
        # update a case group
        response = self.client().patch('/cases/10-29',
            json={ "age_group": "18-29",
                "total_num_case": 25000,
                "total_num_death": 12,
                "total_num_intensivecare": 200}, headers={"Authorization": "Bearer {}".format(self.admin)})
        data = json.loads(response.data)
        #print(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['case'])

    def test_400_update_case(self):
        response = self.client().patch(
            '/cases/1-5',
            json={
                "age_group": "1-5",
                "total_num_case": 25000,
                "total_num_death": 12,
                "total_num_intensivecare": 200
            },
            headers={
                "Authorization": "Bearer {}".format(self.admin)})
        data = json.loads(response.data)
        #print(data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Please provide correct age group!')

    def test_delete_case(self):
        res = self.client().delete('/cases/18-29', headers={"Authorization": "Bearer {}".format(self.admin)})
        data = json.loads(res.data)
        #print(data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 10)

    def test_404_delete_case(self):
        res = self.client().delete('/cases/', headers={"Authorization": "Bearer {}".format(self.admin)})
        data = json.loads(res.data)
        #print(data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Resource not found!")

     # Vaccination
    def test_create_vaccin(self):
        new_cases = {"age_group": "80-89",
                     "kommun_namn": "TEST_Vallentuna",
                     "num_fully_vaccinated": 1545,
                     "num_minst_1_dos": 1095,
                     "population": 1243,
                     "proportion_of_fully_vaccinated": 0.9070290390000001,
                     "proportion_of_minst_1_dos": 0.9780290390000001,
                     "region": "Stockholm",
                     "vaccination_info_id": 10}

        res = self.client().post('/vaccinations', json=new_cases, headers={"Authorization": "Bearer {}".format(self.admin)})
        data = json.loads(res.data)
        #print(data)
        # check if the vaccin info has been created or not
        vaccin = Vaccination.query.filter_by(id=new_cases['vaccination_info_id']).one_or_none()
        #print(vaccin)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(vaccin)

    def test_404_vaccin_creation_failure(self):
        # create a new vaccin
        res = self.client().post('/vaccinations/', headers={"Authorization": "Bearer {}".format(self.admin)})
        data = json.loads(res.data)
        #print(data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found!')

    def test_fetch_top10_vaccin(self):
        res = self.client().get('/vaccinations', headers={"Authorization": "Bearer {}".format(self.admin)})
        data = json.loads(res.data)
        #print(data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_fetch_top10_vaccin(self):
        res = self.client().get('/vaccinations/', headers={"Authorization": "Bearer {}".format(self.user)})
        data = json.loads(res.data)
        #print(data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found!')

    def test_fetch_vaccin_by_id(self):
        res = self.client().get('/vaccinations/11', headers={"Authorization": "Bearer {}".format(self.admin)})
        data = json.loads(res.data)
        #print(data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_vaccin(self):
        res = self.client().delete('/vaccinations/10', headers={"Authorization": "Bearer {}".format(self.admin)})
        data = json.loads(res.data)
        #print(data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 10)

    def test_404_delete_vaccin(self):
        res = self.client().delete('/vaccinations/', headers={"Authorization": "Bearer {}".format(self.admin)})
        data = json.loads(res.data)
        #print(data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Resource not found!")
        
     # Roles
    def test_user(self):
        res = self.client().get('/', headers={'Authorization': 'Bearer {}'.format(self.user)})
        data = res.get_data(as_text=True)
        if 'User' in data:
            self.assertEqual(res.status_code, 200)
            self.assertIn("Authorization", res.headers['Access-Control-Allow-Headers'])

    def test_admin(self):
        res = self.client().get('/', headers={'Authorization': 'Bearer {}'.format(self.admin)})
        data = res.get_data(as_text=True)
        if 'Admin' in data:
            self.assertEqual(res.status_code, 200)
            self.assertIn("Authorization",
                res.headers['Access-Control-Allow-Headers'])

    def test_vaccin_no_auth(self):
        res = self.client().get('/vaccinations', json={})
        data = res.get_data(as_text=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn('Authorization header is missing.', data)
        self.assertIsNone(res.headers.get('Authorization'))

    def test_cases_no_auth(self):
        res = self.client().get('/cases', json={})
        data = res.get_data(as_text=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn('Authorization header is missing.', data)
        self.assertIsNone(res.headers.get('Authorization'))

if __name__ == "__main__":
    unittest.main()
    #app.run(host='0.0.0.0')
