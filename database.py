from sqlalchemy import create_engine, text
import os

db_connection_string = os.environ["DB_CONNECTION_STRING"]
engine = create_engine(db_connection_string,
                       connect_args={"ssl": {
                         "ssl_ca": "/etc/ssl/cert.pem"
                       }})


def load_jobs_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("select * from jobs"))
    print("type(result):", type(result))

    result_all = result.fetchall()
    print("type(result_all):", type(result_all))

    # Convert each row into a list of dictionaries
    result_list = []
    for row in result_all:
      result_list.append(dict(zip(result.keys(), row)))

    print("type(result_list):", type(result_list))
    return result_list
