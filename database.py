from sqlalchemy import create_engine, text, bindparam

import os

db_connection_string = os.environ["DB_CONNECTION_STRING"]
engine = create_engine(db_connection_string,
                       connect_args={"ssl": {
                         "ssl_ca": "/etc/ssl/cert.pem"
                       }})

# The with engine.connect() as conn: statement establishes a connection to the database using the engine object and creates a connection object conn.
def load_jobs_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("select * from jobs")) # The text function from SQLAlchemy is used to create a SQL expression object representing the query.
    print("type(result):", type(result))

    result_all = result.fetchall()
    print("type(result_all):", type(result_all))

    # Convert each row into a list of dictionaries
    result_list = []
    for row in result_all:
      result_list.append(dict(zip(result.keys(), row)))
      #The result.keys() returns a list of column names from the result set.
#   zip(result.keys(), row) pairs each column name with the corresponding value from the row

    print("type(result_list):", type(result_list))
    return result_list

# The bindparams method is called on the query object to define a parameter for the query.
# bindparam("id", id) creates a bind parameter named "id" with the value id. The id variable holds the specific ID value.
def load_job_from_db(id):
  with engine.connect() as conn:
    query = text("select * from jobs where id = :id")
    bound_query = query.bindparams(bindparam("id", id))

    result = conn.execute(bound_query)

    rows = result.fetchall()
    if len(rows) == 0:
      return None
    else:
      return dict(zip(result.keys(), rows[0]))


def add_application_to_db(job_id, data):
  with engine.connect() as conn:
    query = text(
      "INSERT INTO applications (job_id, full_name, email, linkedin_url, education, work_experience, resume_url) VALUES (:job_id, :full_name, :email, :linkedin_url, :education, :work_experience, :resume_url)"
    )

    conn.execute(
      query, {
        'job_id': job_id,
        'full_name': data['full_name'],
        'email': data['email'],
        'linkedin_url': data['linkedin_url'],
        'education': data['education'],
        'work_experience': data['work_experience'],
        'resume_url': data['resume_url']
      })


def authenticate_user(email, password):
  with engine.connect() as conn:
    query = text(
      "SELECT * FROM user WHERE email = :email AND password = :password")
    bound_query = query.bindparams(email=email, password=password)

    result = conn.execute(bound_query)
    user = result.fetchone()

    if user:
      # Convert the user row into a dictionary
      user_dict = dict(zip(result.keys(), user))
      return user_dict
    else:
      return None
