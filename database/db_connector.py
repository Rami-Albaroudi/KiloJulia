'''
Citation for the following code:
Date: 09/05/2024
Authors: Rami Albaroudi and Mohamed Saud, Group 13
Adapted from: https://github.com/osu-cs340-ecampus/flask-starter-app
'''
import MySQLdb
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# Retrieve credentials from .env file
host = os.environ.get("340DBHOST")
user = os.environ.get("340DBUSER")
passwd = os.environ.get("340DBPW")
db = os.environ.get("340DB")

# Connect to MySQL database using credentials from .env file
def connect_to_database(host = host, user = user, passwd = passwd, db = db):
    db_connection = MySQLdb.connect(host,user,passwd,db)
    return db_connection

# Function used to execute query on the database with the query as a parameter
def execute_query(db_connection = None, query = None, query_params = ()):
    # Check if database connection was successfully established
    if db_connection is None:
        print("No connection to the database found! Have you called connect_to_database() first?")
        return None

    # Check if query is blank/missing
    if query is None or len(query.strip()) == 0:
        print("query is empty! Please pass a SQL query in query")
        return None

    # Execute the query and return the data
    print("Executing %s with %s" % (query, query_params));
    cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(query, query_params)
    db_connection.commit();
    return cursor