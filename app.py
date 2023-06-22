from flask import Flask, render_template, jsonify, request
from database import load_jobs_from_db, load_job_from_db, add_application_to_db

app = Flask(__name__)


@app.route("/")
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
        return render_template('application_submitted.html', job=job, application=data)
    else:
        # Handle GET request for apply form
        return render_template('application_submitted.html', job=job, application={})






if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
