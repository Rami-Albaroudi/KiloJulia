from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import os
import json
import database.db_credentials as db_creds
import database.db_connector as db_con

# Configuration

app = Flask(__name__)
app.config['MYSQL_HOST'] = db_creds.host
app.config['MYSQL_USER'] = db_creds.user
app.config['MYSQL_PASSWORD'] = db_creds.passwd
app.config['MYSQL_DB'] = db_creds.db
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

mysql = MySQL(app)

db_connection = db_con.connect_to_database()

# Routes 

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/staff', methods=['GET', 'POST'])
def staff():
    query = "SELECT * FROM Staff;"
    cursor = db_con.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template("staff.j2", staff=results)


@app.route('/clients')
def clients():
    query = "SELECT * FROM Clients;"
    cursor = db_con.execute_query(db_connection=db_connection, query=query)
    results = cursor.fetchall()
    return render_template("clients.j2", clients=results)

@app.route('/staffclients')
def staffclients():
    # Query to fetch staff and client names along with their IDs
    query = """
    SELECT sc.staffID, s.staffName, sc.clientID, c.clientName
    FROM StaffClients sc
    JOIN Staff s ON sc.staffID = s.staffID
    JOIN Clients c ON sc.clientID = c.clientID;
    """
    assignments = db_con.execute_query(db_connection=db_connection, query=query).fetchall()

    # Fetch lists of all staff and clients for dropdowns or other uses
    staff_query = "SELECT staffID, staffName FROM Staff;"
    client_query = "SELECT clientID, clientName FROM Clients;"
    staff = db_con.execute_query(db_connection=db_connection, query=staff_query).fetchall()
    clients = db_con.execute_query(db_connection=db_connection, query=client_query).fetchall()

    return render_template("staffclients.j2", staff=staff, clients=clients, assignments=assignments)


@app.route('/trackeddays')
def tracked_days():
    # Fetch tracked days and client names for the dropdown
    tracked_days_query = """
    SELECT td.*, c.clientName
    FROM TrackedDays td
    JOIN Clients c ON td.clientID = c.clientID;
    """
    clients_query = "SELECT clientID, clientName FROM Clients;"
    
    tracked_days = db_con.execute_query(db_connection=db_connection, query=tracked_days_query).fetchall()
    clients = db_con.execute_query(db_connection=db_connection, query=clients_query).fetchall()
    
    return render_template("trackeddays.j2", tracked_days=tracked_days, clients=clients)


@app.route('/foods')
def foods():
    query = "SELECT * FROM Foods;"
    cursor = db_con.execute_query(db_connection=db_connection, query=query)
    foods = cursor.fetchall() 
    return render_template("foods.j2", foods=foods)


@app.route('/foodentries')
def foodentries():
    query = "SELECT * FROM FoodEntries;"
    cursor = db_con.execute_query(db_connection=db_connection, query=query)
    foodentries = cursor.fetchall() 
    return render_template("foodentries.j2", foodentries=foodentries)

@app.route('/exerciseentries')
def exerciseentries():
    query = "SELECT * FROM ExerciseEntries;"
    cursor = db_con.execute_query(db_connection=db_connection, query=query)
    exerciseentries = cursor.fetchall() 
    return render_template("exerciseentries.j2", exerciseentries=exerciseentries)

# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 1867)) 
    app.run(port=port, debug=True)