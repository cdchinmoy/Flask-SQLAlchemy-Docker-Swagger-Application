# Flask Assignment

Flask application to manage the patient appointment

----------------------------------------------------

## STEP 1 

Install requirements.txt file <br>
Command: pip install -r requirements.txt

## STEP 2

Setup database configuration inside project filename: __init__.py <br>
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://dbuser:dbpassword@localhost/dbname"

## STEP 3

Database migration command: <br>
    1. python manage.py db init <br>
    2. python manage.py db migrate <br>
    3. python manage.py db upgrade

## STEP 4

Run: python run.py

----------------------------------------------------

## Swagger Endpoint URL:
localhost:5000/swagger

1. Register a user
2. Login with the credentials 
3. After a successful request token get generated and returned.
4. To access and submit data need to enter token for user authentication.





