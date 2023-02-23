# GPA_REST_API
This is the backend of my Academic record tracker web app. I created it using Python and Flask
link to the web app - < will be inserted when finished >

## Why? ##
As a second year computer science student, I was looking for an app that will be able to record my courses and calculate the GPA accordingly.
unfortunatly, there weren't any. So I created my own, in which you are able to register as a user and then create, modify and delete courses you are taking.
This way, you can keep track of your courses, and play with the GPA accordingly to know if you need that second exam ;)

## how? ##
First of all, using Jose Salvatierra course on Udemy about Flask and python, I was able to acquire the necessary knowledge.

1. I used SQLAlchemy and Flask-SQLAlchemy extension to create the database models I needed.
2. Using marshmallow I created schemas.
3. Using Flask-Smorest Blueprints and swagger-ui, I have created the endpoints with documentation.
4. I used Flask-JWT-Extended for user registration, authentication, certein endpoints protection, and made sure to add revoked tokens to a blocklist.
5. Used Flask-Migrate and Alembic for data migration.
