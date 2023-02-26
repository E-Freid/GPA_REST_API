# GPA REST API

This is a simple REST API for calculating and storing GPAs. The API is built using Flask and various other technologies.

## Technology

The GPA REST API uses the following technologies:

- Flask: A micro web framework written in Python.
- Flask-SQLAlchemy: A Flask extension that adds SQLAlchemy support to your Flask application.
- SQLAlchemy: A SQL toolkit and Object-Relational Mapping (ORM) library for Python.
- python-dotenv: A zero-dependency module that loads environment variables from a .env file.
- Flask-Smorest: A Flask extension for building REST APIs.
- Flask-JWT-Extended: A Flask extension that adds support for JSON Web Tokens (JWTs) to your Flask application.
- passlib: A Python library for hashing and verifying passwords.
- Gunicorn: A Python WSGI HTTP Server for UNIX.
- Flask-Migrate: A Flask extension that handles SQLAlchemy database migrations.
- psycopg2-binary: A PostgreSQL database adapter for Python.
- Flask-Cors: A Flask extension for handling Cross-Origin Resource Sharing (CORS) requests.

## Database

The GPA REST API uses a PostgreSQL database to store user and GPA data. SQLAlchemy is used as the ORM library to interact with the database.

## Security

The API uses JSON Web Tokens (JWTs) for authentication and authorization. Passlib is used to hash and verify user passwords. The API also uses a token blocklist to revoke JWTs that have been compromised or are no longer needed.

## endpints
### Authentication
- `POST /register` - Create a new user account.
- `POST /login` - Login with an existing account and get an access token.
- `POST /logout` - Logout the currently authenticated user.
- `POST /cleanup` - Clean expired tokens from the blocklist (must contain special key in header). refer to the GET STARTED and to the `/cleanup` endpoint code in user.py.

### Courses
- `GET /user/course` - Get a list of courses belonging to the authenticated user. Endpoint must contain JWT token.
- `POST /user/course` - Create a new course for the authenticated user. Endpoint must contain JWT token.
- `GET /user/course/int:course_id` - Get details of a specific course belonging to the authenticated user. Endpoint must contain JWT token.
- `PUT /user/course/int:course_id` - Update details of a specific course belonging to the authenticated user. Endpoint must contain JWT token.
- `DELETE /user/course/int:course_id` - Delete a specific course belonging to the authenticated user. Endpoint must contain JWT token.

## Getting Started

1. Clone the repository to your local machine: `git clone https://github.com/your_username/gpa-rest-api.git`.
2. Create a virtual environment: `python3 -m venv venv`.
3. Activate the venv: `source venv/bin/activate`.
4. Install the project dependencies: `pip install -r requirements.txt`.
5. create a `.env` file and add the following environment variables:
  - `DATABASE_URL = your_database_uri_here`
  - `JWT_SECRET_KEY = your_jwt_secret_key_here`
  - `CLEANUP_SECRET_KEY = your_cleanup_secret_key`
6. initialize, migrate and upgrade the database:
  - `flask db init`
  - `flask db migrate`
  - `flask db upgrade`
 7. Run the api: `flask run`. The app will be accessible at `http://localhost:5000/`
