# Full Stack API Final Project


## Full Stack COVID_SE

## Getting Started

[Fork](https://help.github.com/en/articles/fork-a-repo) the [project repository](https://github.com/udacity/FSND/blob/master/projects/02_trivia_api/starter) and [Clone](https://help.github.com/en/articles/cloning-a-repository) your forked repository to your machine. Work on the project locally and make sure to push all your changes to the remote repository before submitting the link to your repository in the Classroom.
>Once you're ready, you can submit your project on the last page.

### Installing Dependencies

#### Backend

`pip install -r requirements.txt`

#### Frontend
open '\frontend' directory and run:

`npm install`

### Running the server

#### Backend
open '\backend' directory and run:

  ```
  export FLASK_APP=app.py
  export FLASK_ENV=development
  flask run  --reload
  ```

#### Frontend
open '\frontend' directory and run:

`npm start`

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
 - Request all the categories and the questions;
 - Search questions based on a specific string;
 - Create/Delete questions;
 - Find a random question in any given context.

Base URL:
 - Backend (local host): [http://127.0.0.1:5000](http://127.0.0.1:5000/)
 - Frontend: [http://localhost:3000](http://localhost:3000) 

### Endpoints

#### GET /cases OR GET /cases/<\string:agegroup\>

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
    
#### GET /vaccinations

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
     

#### POST /cases

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


#### PATCH /cases/<\string:agegroup\>

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


#### DELETE /cases

- Delete a case by age group 
- Sample: `curl http://127.0.0.1:5000/cases/18-29 -X DELETE`<br>

        {
          "deleted_age_group": "18-29", 
          "success": true
        }                    

#### GET /vaccinations/\<int:id\>

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

### Error Handling

There are 4 types of errors included in this API (400, 404, 422, 500). Errors will be returned as JSON to view, 
for instance, the error 404 will be presented as :<br>

    {
        "success": False,
        "error": 404,
        "message": "resource not found"
    }

### Note:
1. Auth0 configuration: 
    - URL: https://fwddev.eu.auth0.com/authorize?audience=http://localhost:5000&response_type=token&client_id=akqmzDqru4tisoJFJikJHobPcSAZTVwe&redirect_uri=http://localhost:8100/tabs/user-page
    - Users: 
    
        ```
        - admin: admin@covid.se 
          token: Coffee1234 
          Active JWT: eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im9mU0poLW1tSm1EczNpcFBiRW9KQyJ9.eyJpc3MiOiJodHRwczovL2Z3ZGRldi5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjE3NTk2Yzk1ZDNkOWQwMDcwZjA4Zjk0IiwiYXVkIjoiaHR0cDovL2xvY2FsaG9zdDo1MDAwIiwiaWF0IjoxNjM1NzUxODczLCJleHAiOjE2MzU3NTkwNzMsImF6cCI6ImFrcW16RHFydTR0aXNvSkZKaWtKSG9iUGNTQVpUVndlIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6ZHJpbmtzIiwiZ2V0OmRyaW5rcy1kZXRhaWwiXX0.RYOkkDAT5od1zpFeDj3QsJqI-TMD5FzVY4z8uzyZjN-yBbzReIXVQz1IbDrxeaZ-AKtGXgabOxaQzf9-k0uC1wRH-BlZokVrtGm4amv-xwllvM00jkasIb4wTzA8ZhSULSO5gQjZ5TDhYpnqhTI09hHjnlegGp-Lx3T6qqAxApCoLBXnF-30G0_ro0FzzuPyuZ1BUHpWjT2P6umIi6zyTIOqw8uYhatCrDh6kKaaBdNV0wLc6X9qrF0oRRIR8VuTG-vI-CvEgWgc-IcEJV7tavx6MYd5VL5pcLFspOY2SMMSwAHxW5YX5b6xvh0ma5fjbkZzCnoTK2q8w4KGnk7DwQ

        - user: user@covid.se 
          token: Coffee5678
          Active JWT: eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im9mU0poLW1tSm1EczNpcFBiRW9KQyJ9.eyJpc3MiOiJodHRwczovL2Z3ZGRldi5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjE3NTk3ZTdlZDNhMjkwMDY4YjY5YTMxIiwiYXVkIjoiaHR0cDovL2xvY2FsaG9zdDo1MDAwIiwiaWF0IjoxNjM1NzEyNTYwLCJleHAiOjE2MzU3MTk3NjAsImF6cCI6ImFrcW16RHFydTR0aXNvSkZKaWtKSG9iUGNTQVpUVndlIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6ZHJpbmtzIiwiZ2V0OmRyaW5rcyIsImdldDpkcmlua3MtZGV0YWlsIiwicGF0Y2g6ZHJpbmtzIiwicG9zdDpkcmlua3MiXX0.hXWjDRFDRQQcpM8gCbTA8ZtRF4LQuaOhjl_sRGeUsWYDX_MMYHB9YOvIDFAyf75P6eJk5R-66A9fP91IsybCvkTpBsnCfqK6gqmrGsI_yoKn05Rjl7MxZFBGDmCoDkmqGpVJgCGUedkwPIpo8ZyaoewsA97ZxbORJl0ftH8CersPUMiys1QsQCvcoOQKc2Yoyx4WkA264KyxmC9E_d5pbZ4Zuva-8rN3H-m78UZo-cin5v0qhFS6Rr-btXPXmelqy6THSfZt9aRAnNUkNwJLjeJHBgXn0sXh4tQQqlqOkGQ3an59f3dwxjhPs9O83q8Q4OYjCOfZlyc_JuFlShKCQg
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
- https://github.com/facebook/create-react-app/issues/9619
- https://www.outsystems.com/forums/discussion/46385/how-to-concatenate-a-string-to-html-string/
- https://www.jhipster.tech/tips/028_tip_pgadmin_heroku.html



