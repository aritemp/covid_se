# Full Stack API Final Project


## Full Stack COVID_SE 2021

## Introduction

This app intends to show Covid19 information in Sweden, including cases information across different age groups and 
vaccination information across different age groups and regions.

## Getting Started

### Installing Dependencies

#### Backend

`pip install -r requirements.txt`

### Running the server

Open the directory and run:

  ```
  export FLASK_APP=app.py
  export FLASK_ENV=development
  flask run  --reload
  ```

### Testing the app

```
dropdb covid
createdb covid
psql covid < covid.psql
python test_app.py
```

## API Reference

### Getting Started

This API can help to:
 - Request all the available cases and vaccination info in Sweden;
 - Create/Modify/Delete cases/vaccination info based on the roles.
 
There are two roles available:
    - Admin
        - Can perform all the available activities, like viewing, modifying, creating, deleting cases and vaccination info.
    - User
        - Can only view all the cases and vaccination info.
    - No one can modify the vaccination info.

    |   Roles   |   Permissions |
    |   :---    |     :---      |
    |   Admin   | `get:cases` `get:case_agegroup` `patch:cases`  `post:cases` `delete:cases` `get:vaccin` `post:vaccin` `delete:vaccin`|
    |   User    | `get:cases` `get:case_agegroup` `get:vaccin`|
     --------------------------------------------------------------------------------------
    |    Permissions     |          Description          |
    |        :---        |             :---              |
    |  `get:cases`       |     Read the cases in general |
    | `get:case_agegroup`| Read the details of the case info by the age group | 
    |  `post:cases`      |       Add new case info       |  
    |  `patch:cases`     |         Modify the case by the age group       |  
    |  `delete:cases`    |    Delete the case info by the age group       | 
    |  `get:vaccin`      | Read the top 10 fully vaccinated groups info and the specific vaccination info by id |  
    |  `post:vaccin`     |   Add new vaccination info    |  
    |  `delete:vaccin`   | Delete vaccination info by id |     
    

## Getting Started

Base URL:
 - [https://covid-se2021.herokuapp.com](https://covid-se2021.herokuapp.com)
 - [http://127.0.0.1:5000](http://127.0.0.1:5000)

### Endpoints

##### GET /cases OR GET /cases/<\string:agegroup\>

- Return a list of cases.
- Sample: `curl http://127.0.0.1:5000/cases`<br>

         {
            "cases_info": [
                 {
              "age_group": "10-19", 
              "total_num_case": 163093, 
              "total_num_death": 5, 
              "total_num_intensivecare": 53
            }, 
            {
              "age_group": "20-29", 
              "total_num_case": 203508, 
              "total_num_death": 25, 
              "total_num_intensivecare": 215
            }, 
            {
              "age_group": "30-39", 
              "total_num_case": 206199, 
              "total_num_death": 46, 
              "total_num_intensivecare": 368
            }, 
            {
              "age_group": "40-49", 
              "total_num_case": 210361, 
              "total_num_death": 123, 
              "total_num_intensivecare": 865
            }, 
            {
              "age_group": "50-59", 
              "total_num_case": 180902, 
              "total_num_death": 389, 
              "total_num_intensivecare": 1707
            }, 
            {
              "age_group": "60-69", 
              "total_num_case": 91334, 
              "total_num_death": 1063, 
              "total_num_intensivecare": 2251
            }, 
            {
              "age_group": "70-79", 
              "total_num_case": 42062, 
              "total_num_death": 3367, 
              "total_num_intensivecare": 1959
            }, 
            {
              "age_group": "80-89", 
              "total_num_case": 25541, 
              "total_num_death": 6093, 
              "total_num_intensivecare": 436
            }, 
            {
              "age_group": ">=90", 
              "total_num_case": 11394, 
              "total_num_death": 3896, 
              "total_num_intensivecare": 10
            }, 
            {
              "age_group": "Uppgift-saknas", 
              "total_num_case": 148, 
              "total_num_death": 0, 
              "total_num_intensivecare": 1
            }
          ], 
          "success": true
        }
    
    
- Sample: `curl http://127.0.0.1:5000/cases/10-19`<br>

    {
        "cases_info": {
        "age_group": "10-19", 
        "total_num_case": 163093, 
        "total_num_death": 5, 
        "total_num_intensivecare": 53
        }, 
    "success": true
    }
    
##### GET /vaccinations

- Return a list of top 10 number of fully vaccinated age group and region.
* Sample: `curl http://127.0.0.1:5000/vaccinations`<br>
    
       {
      "success": true, 
      "top 10 fully vaccinated [age_group, region, total_number_of_fully_vaccinated]": [
        [
          "50-59", 
          "Stockholm", 
          259748
        ], 
        [
          "40-49", 
          "Stockholm", 
          257359
        ], 
        [
          "30-39", 
          "Stockholm", 
          251679
        ], 
        [
          "60-69", 
          "Stockholm", 
          196977
        ], 
        [
          "50-59", 
          "V\u00e4stra G\u00f6taland", 
          188190
        ], 
        [
          "70-79", 
          "Stockholm", 
          174610
        ], 
        [
          "30-39", 
          "V\u00e4stra G\u00f6taland", 
          168106
        ], 
        [
          "40-49", 
          "V\u00e4stra G\u00f6taland", 
          167728
        ], 
        [
          "60-69", 
          "V\u00e4stra G\u00f6taland", 
          166417
        ], 
        [
          "70-79", 
          "V\u00e4stra G\u00f6taland", 
          154538
        ]
      ]
    }
     

##### POST /cases

- Add a new case
    - Sample: `curl http://127.0.0.1:5000/cases -X POST -H "Content-Type: application/json" -d '{
               "age_group": "18-29", 
    "total_num_case": 273093, 
    "total_num_death": 12, 
    "total_num_intensivecare": 200
    }'`<br>
           
       {
          "case_age_group": "18-29", 
          "new case": {
            "age_group": "18-29", 
            "total_num_case": 273093, 
            "total_num_death": 12, 
            "total_num_intensivecare": 200
          }, 
          "success": true
        }


##### PATCH /cases/<\string:agegroup\>

- Modify a case by age group 
- Sample: `curl http://127.0.0.1:5000/cases/18-29 -X PATCH -H "Content-Type: application/json" -d '{
               "age_group": "18-29", 
    "total_num_case": 25000, 
    "total_num_death": 12, 
    "total_num_intensivecare": 200
    }'`<br>

        {
          "case": {
            "age_group": "18-29", 
            "total_num_case": 25000, 
            "total_num_death": 12, 
            "total_num_intensivecare": 200
          }, 
          "success": true
        }     


##### DELETE /cases

- Delete a case by age group 
- Sample: `curl http://127.0.0.1:5000/cases/18-29 -X DELETE`<br>

        {
          "deleted_age_group": "18-29", 
          "success": true
        }                    

##### GET /vaccinations/\<int:id\>

 - Get vaccination info by vaccination id
 - Sample: `curl http://127.0.0.1:5000/vaccinations/2`<br>

         {
          "success": true, 
          "vaccination": {
            "age_group": "30-39", 
            "kommun_namn": "Upplands V\u00e4sby", 
            "num_fully_vaccinated": 4341, 
            "num_minst_1_dos": 4976, 
            "population": 7088, 
            "proportion_of_fully_vaccinated": 0.612443567, 
            "proportion_of_minst_1_dos": 0.702031603, 
            "region": "Stockholm", 
            "vaccination_info_id": 2
          }
        }

#### Error Handling

There are 4 types of errors included in this API (400, 404, 422, 500). Errors will be returned as JSON to view, 
for instance, the error 404 will be presented as :<br>

    {
        "success": False,
        "error": 404,
        "message": "resource not found"
    }

### Auth0 configuration:
 
    - URL: https://fwddev.eu.auth0.com/authorize?audience=se_covid2021&response_type=token&client_id=9P90EvszrUfHRmp2AKTOiQsYUIbykQIn&redirect_uri=https://covid-se2021.herokuapp.com/callback
    - Users: 
    
        ```
        - admin: admin@covid.se 
          token: Covid1234 
          Active JWT: eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im9mU0poLW1tSm1EczNpcFBiRW9KQyJ9.eyJpc3MiOiJodHRwczovL2Z3ZGRldi5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjE5MGQ4NGZhM2EzODYwMDZhYjVlNzY5IiwiYXVkIjoic2VfY292aWQyMDIxIiwiaWF0IjoxNjM3NDA2NTEwLCJleHAiOjE2Mzc0MTM3MTAsImF6cCI6IjlQOTBFdnN6clVmSFJtcDJBS1RPaVFzWVVJYnlrUUluIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6Y2FzZXMiLCJkZWxldGU6dmFjY2luIiwiZ2V0OmNhc2VfYWdlZ3JvdXAiLCJnZXQ6Y2FzZXMiLCJnZXQ6dmFjY2luIiwicGF0Y2g6Y2FzZXMiLCJwb3N0OmNhc2VzIiwicG9zdDp2YWNjaW4iXX0.UwI9v6rFN7Qf5KXNyA4T3YmOK2Ow_Ph-QMnHOgo9vFmMtOLQU3bnWrT34L3lBME1MpZ_aCS82h22HHtU4F46ZNwS1Ff-NCrUu_PijpKYH6QsLjpMAtV_6dVLyfEwLgvoK-uXbsPOr1lg28AFTk1p6vlsmz-9uNBH_AI15ayWWiM3x84UhIqSXpiFeJa4xcJHCT1CEfxTxZdttvGFoH6AWXAQUWiGFBZk8uzTh2HDi7kD9EVguKEsxJpI9Cbn9Gc91_FfUuClCOixCD3qiukh-kXa2kH2UmoPjO2pRKFlxsGo0xNpHPV9baNRVGj1C3tju9p-7nTsqRK-J2DzmQ3EBw

        - user: user@covid.se 
          token: Covid5678
          Active JWT: eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im9mU0poLW1tSm1EczNpcFBiRW9KQyJ9.eyJpc3MiOiJodHRwczovL2Z3ZGRldi5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjE5MGQ3Y2Y0NzBkMDcwMDY5MzA5MDA4IiwiYXVkIjoic2VfY292aWQyMDIxIiwiaWF0IjoxNjM3NDA2NjAyLCJleHAiOjE2Mzc0MTM4MDIsImF6cCI6IjlQOTBFdnN6clVmSFJtcDJBS1RPaVFzWVVJYnlrUUluIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6Y2FzZV9hZ2Vncm91cCIsImdldDpjYXNlcyIsImdldDp2YWNjaW4iXX0.FecdM2g3stA22UA_8ki4wk63Hqh5U5VD5Uz7CF0BiPxNiD8EuE18H3eqrNNKGvCTspirf2NSlu43Pceqs7q6B7OkqnS5bsAuT9XFhc2Yyc7SkeejsO1FjZHsv-csUkp5vWQ_yQAxOJpW5kpe_XquTuGV67x5uKpAboLHvduGsT38fPBoLgBXYJueEPfG4bmZwyN4tRdPzMPMwV7mPU6TPzg6UBpnYSNwjCObd9GcCBtNLcj96gwlnbMFkov7Pauzbc8Y1K-Yp2NMJsO914MpisJ43DIw8TvvljPPDZC97C6Ve7td1Ec-2Dksg5LGNH11bvWDfd1Su5Wb-3QxP3SK4g
        ```
        
## Authors

Arianna E.

## References

- https://classroom.udacity.com/nanodegrees/nd0044/parts/a379cb3f-af2f-46c8-8303-20c1633b2aec
- https://www.postgresqltutorial.com/import-csv-file-into-posgresql-table/
- https://til.cybertec-postgresql.com/post/2019-09-12-%22PostgreSQL-CSV-Import:-missing-data-for-column-%22...%22%22/
- https://chartio.com/resources/tutorials/how-to-change-a-user-to-superuser-in-postgresql/
- https://stackoverflow.com/questions/40918479/querying-with-function-on-flask-sqlalchemy-model-gives-basequery-object-is-not-c
- https://github.com/udacity/cd0037-API-Development-and-Documentation-exercises/blob/master/4_TDD_Review/backend/flaskr/__init__.py
- https://github.com/morphocluster/morphocluster/tree/master/migrations
- https://www.jhipster.tech/tips/028_tip_pgadmin_heroku.html
- https://github.com/facebook/create-react-app/issues/9619
- https://www.outsystems.com/forums/discussion/46385/how-to-concatenate-a-string-to-html-string/
- https://github.com/auth0-samples/auth0-python-web-app/blob/master/01-Login/server.py
- https://auth0.com/docs/quickstart/webapp/python/01-login
- https://docs.djangoproject.com/en/2.1/ref/templates/language/#template-inheritance
- https://books.google.se/books?id=GedDDwAAQBAJ&pg=PA194&lpg=PA194&dq=def+callback_handling():+++++++++++++if+session.get(%22token%22):&source=bl&ots=2ns8Qtl4-_&sig=ACfU3U0Z8ZnwDKyGhHpUlhcVmpfi-Ti-sQ&hl=sv&sa=X&ved=2ahUKEwiH8fTEyKf0AhViwosKHRtADRsQ6AF6BAgCEAM#v=onepage&q=def%20callback_handling()%3A%20%20%20%20%20%20%20%20%20%20%20%20%20if%20session.get(%22token%22)%3A&f=false
- https://github.com/auth0-samples/auth0-python-web-app/tree/master/01-Login
- https://python-adv-web-apps.readthedocs.io/en/latest/flask_forms.html
- Data source:
    - https://www.folkhalsomyndigheten.se/smittskydd-beredskap/utbrott/aktuella-utbrott/covid-19/statistik-och-analyser/bekraftade-fall-i-sverige/
    - https://www.folkhalsomyndigheten.se/smittskydd-beredskap/utbrott/aktuella-utbrott/covid-19/statistik-och-analyser/statistik-over-registrerade-vaccinationer-covid-19/
