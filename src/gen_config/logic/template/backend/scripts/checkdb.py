import sys
import time
import logging

import psycopg2

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
logging.info("Checking if table 'django_migrations' exists.")
logging.info("If you want to skip this, just set the environment var")
logging.info("TAIGA_SKIP_DB_CHECK=True on docker-compose.yml on <backend> service.")
CONNECTION_STRING = "dbname='{}' user='{}' host='{}' password='{}'".format(
    '{{POST_GRES_SQL_NAME}}',
    '{{POST_GRES_SQL_USER}}',
    '{{POST_GRES_SQL_HOST}}',
    '{{POST_GRES_SQL_PASSWORD}}',
)
LIMIT_RETRIES = {{BACK_END_DB_CHECK_LIMIT_RETRIES}}
SLEEP_INTERVAL = {{BACK_END_DB_CHECK_SLEEP_INTERVAL}}


def postgres_connection(connection_string, retry_counter=1):
    try:
        connection = psycopg2.connect(connection_string)
    except psycopg2.OperationalError as e:
        if retry_counter > LIMIT_RETRIES:
            logging.error("connection_string:%s", connection_string)
            logging.error("CAN'T CONNECT TO POSTGRES")
            logging.error("Check your connection settings.")
            logging.error("Or increase (in docker-compose.yml):")
            logging.error(
                "DB_CHECK_SLEEP_INTERVAL / DB_CHECK_LIMIT_RETRIES."
            )
            logging.error("Exception messsage: {e}")
            sys.exit(1)
        else:
            logging.warning("Can't connect to Postgres. Will try again...")
            time.sleep(SLEEP_INTERVAL)
            retry_counter += 1
            return postgres_connection(connection_string, retry_counter)
    return connection


cursor = postgres_connection(CONNECTION_STRING).cursor()
cursor.execute(
    "select exists(select * from information_schema.tables where table_name=%s)",
    ('django_migrations',)
)
if not cursor.fetchone()[0]:
    logging.info("So, it seems like it's the first time you run the <backend>")
    logging.info("service for taiga. Will try to:")
    logging.info("1) migrate DB; 2) load initial data; 3) compilemessages")
    print('missing_django_migrations')
