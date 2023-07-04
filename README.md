# jovian-careers-website

The Flask Job Portal Application is a web application that allows users to register, login, view job listings, and apply for jobs.

### Installation
    Install the dependencies: 'pip install -r requirements.txt'

### Configuration

1. Set up the database connection string:
   - Export the database connection string as an environment variable: `export DB_CONNECTION_STRING=your-connection-string`
2. Generate a secret key for session management:
   - Set the secret key as an environment variable: `export SECRET_KEY=your-secret-key`

### Running the Application

1. Run the Flask development server:
   - Execute the following command: `python app.py`
   - The application will be accessible at: `http://localhost:5000`
###  Imports 
from flask import Flask, render_template, jsonify, request, redirect, url_for, session
from database import load_jobs_from_db, load_job_from_db, add_application_to_db, authenticate_user
from sqlalchemy import create_engine, text 
import os


Flask is imported from the flask module, which is the main framework used for building the web application.
render_template is imported from the flask module to render HTML templates.
jsonify is imported from the flask module to generate JSON responses.
request is imported from the flask module to access HTTP request data.
redirect and url_for are imported from the flask module to perform URL redirection.
session is imported from the flask module to store user session data.
load_jobs_from_db, load_job_from_db, add_application_to_db, and authenticate_user are imported from the database module. These functions are  defined in the database.py file and are used for interacting with the database.
create_engine is imported from the sqlalchemy module to create a database connection engine.
text is imported from the sqlalchemy module to define SQL query strings.
os is imported to access operating system-related functionality, such as environment variables.

### Routes

- '/' (Register)
  - GET: Renders the registration form.
  - POST: Processes the registration form data and inserts the user into the database. Redirects to the login page after successful registration.

- '/login'
  - GET: Renders the login form.
  - POST: Processes the login form data, authenticates the user, and stores user information in the session. Redirects to the home page if authentication is successful, otherwise renders the login page with an error message.

- '/home'
  - GET: Renders the home page, displaying a list of job listings retrieved from the database.

- '/api/jobs'
  - GET: Returns a JSON response containing a list of job listings retrieved from the database.

- '/job/<id>'
  - GET: Renders the job details page for the specified job ID. If the job is not found, returns a "Not Found" response.

- '/job/<id>/apply'
  - GET: Renders the job application form for the specified job ID.
  - POST: Processes the job application form data and adds the application to the database. Renders the application submitted page with the job and application details.

### Templates

The application uses the following HTML templates located in the templates directory:

- register.html: Registration form template.
- login.html: Login form template.
- home.html: Home page template, displaying a list of job listings.
- jobpage.html: Job details page template.
- application_submitted.html: Application submitted page template.

### Database Functions

The application relies on several database functions that are imported from the database module:

- load_jobs_from_db(): Retrieves a list of job listings from the database.
- load_job_from_db(id): Retrieves the details of a specific job with the given ID from the database.
- add_application_to_db(id, data): Adds a job application to the database for the specified job ID.
- authenticate_user(email, password): Authenticates a user based on the provided email and password.

These functions should be implemented or imported from another module to ensure proper functionality of the application.

### Security Considerations

- The application uses a secret key (`SECRET_KEY`) to secure the session management. Ensure that the secret key is kept secret and not shared publicly.
- The database connection string is stored as an environment variable (`DB_CONNECTION_STRING`). Ensure that it is properly configured and secure.
- User passwords should be stored securely by using appropriate hashing and salting techniques.

