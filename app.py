from flask import Flask, render_template, jsonify, request, redirect, url_for, session
from database import load_jobs_from_db, load_job_from_db, add_application_to_db, authenticate_user
from sqlalchemy import create_engine, text, bindparam
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

db_connection_string = os.environ["DB_CONNECTION_STRING"]
engine = create_engine(db_connection_string,
                       connect_args={"ssl": {
                         "ssl_ca": "/etc/ssl/cert.pem"
                       }})


@app.route("/", methods=['GET', 'POST'])
def register():
  if request.method == 'POST':
    # Handle registration form submission
    userid = request.form['userid']
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

    # Insert the user data into the database
    with engine.connect() as conn:
      query = text(
        "INSERT INTO user (userid, name, email, password) VALUES (:userid, :name, :email, :password)"
      )
      conn.execute(query, {
        "userid": userid,
        "name": name,
        "email": email,
        "password": password
      })

    return redirect(
      url_for('login'))  # Redirect to login page after successful registration
  else:
    return render_template('register.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if the user is authenticated
        user = authenticate_user(email, password)
        if user:
            # Store user information in the session
            session['user_id'] = user['userid']
            session['email'] = user['email']
            session['name'] = user['name']
            
            return redirect(url_for('hello_jovian'))
        else:
            # User authentication failed
            message = 'Invalid email or password'
            return render_template('login.html', message=message)
    else:
        return render_template('login.html')

@app.route("/home")
def hello_jovian():
  jobs = load_jobs_from_db()
  return render_template('home.html', jobs=jobs)


@app.route("/api/jobs")
def list_jobs():
  jobs = load_jobs_from_db()
  return jsonify(jobs)


@app.route("/job/<id>")
def show_job(id):
  job = load_job_from_db(id)
  if not job:
    return "Not Found", 404
  return render_template('jobpage.html', job=job)


@app.route("/job/<id>/apply", methods=['GET', 'POST'])
def apply_to_job(id):
  job = load_job_from_db(id)  # Load the job data
  if request.method == 'POST':
    data = request.form  # Access form data
    # Process the form data or perform other actions
    add_application_to_db(id, data)
    return render_template('application_submitted.html',
                           job=job,
                           application=data)
  else:
    # Handle GET request for apply form
    return render_template('application_submitted.html',
                           job=job,
                           application={})


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
