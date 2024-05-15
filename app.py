'''
Citation for the following code:
Date: 09/05/2024
Authors: Rami Albaroudi and Mohamed Saud, Group 13
Adapted from https://github.com/osu-cs340-ecampus/flask-starter-app with significant modifications
'''
# Imports
from flask import Flask, render_template, request, redirect, json
from flask_mysqldb import MySQL
import os
import database.db_connector as db

# Configuration
app = Flask(__name__)
app.config['MYSQL_HOST'] = db.host
app.config['MYSQL_USER'] = db.user
app.config['MYSQL_PASSWORD'] = db.passwd
app.config['MYSQL_DB'] = db.db
app.config['MYSQL_CURSORCLASS'] = "DictCursor"
mysql = MySQL(app)

# Routes 
@app.route('/')
@app.route('/index')
def index():
    return render_template("index.j2")

@app.route('/staff', methods=['GET', 'POST'])
def staff():
    query = "SELECT * FROM Staff;"
    cur = mysql.connection.cursor() 
    cur.execute(query)
    staff = cur.fetchall()
    return render_template("staff.j2", staff=staff)

@app.route('/clients')
def clients():
    query = "SELECT * FROM Clients;"
    cur = mysql.connection.cursor()
    cur.execute(query)
    clients = cur.fetchall()
    return render_template("clients.j2", clients=clients)

@app.route('/staffclients')
def staffclients():
    query = """
    SELECT sc.staffID, s.staffName, sc.clientID, c.clientName
    FROM StaffClients sc
    JOIN Staff s ON sc.staffID = s.staffID
    JOIN Clients c ON sc.clientID = c.clientID;
    """
    cur = mysql.connection.cursor()
    cur.execute(query)
    staffclients = cur.fetchall()
    return render_template("staffclients.j2", staffclients=staffclients)

@app.route('/trackeddays', methods=['GET', 'POST'])
def trackeddays():
    if request.method == 'POST':
        search_query = request.form['search_query']
        query = """
        SELECT 
            td.trackedDayID,
            td.clientID,
            td.trackedDayDate,
            (
                SELECT COALESCE(SUM(fe.foodEntryCalories), 0)
                FROM FoodEntries fe
                WHERE fe.trackedDayID = td.trackedDayID
            ) -
            (
                SELECT COALESCE(SUM(ee.exerciseEntryCalories), 0)
                FROM ExerciseEntries ee
                WHERE ee.trackedDayID = td.trackedDayID
            ) AS trackedDayTotalCalories,
            td.trackedDayCalorieTarget,
            td.trackedDayNote,
            c.clientName
        FROM TrackedDays td
        JOIN Clients c ON td.clientID = c.clientID
        WHERE c.clientName LIKE %s;
        """
        cur = mysql.connection.cursor()
        cur.execute(query, ('%' + search_query + '%',))
        trackeddays = cur.fetchall()
    else:
        query = """
        SELECT 
            td.trackedDayID,
            td.clientID,
            td.trackedDayDate,
            (
                SELECT COALESCE(SUM(fe.foodEntryCalories), 0)
                FROM FoodEntries fe
                WHERE fe.trackedDayID = td.trackedDayID
            ) -
            (
                SELECT COALESCE(SUM(ee.exerciseEntryCalories), 0)
                FROM ExerciseEntries ee
                WHERE ee.trackedDayID = td.trackedDayID
            ) AS trackedDayTotalCalories,
            td.trackedDayCalorieTarget,
            td.trackedDayNote,
            c.clientName
        FROM TrackedDays td
        JOIN Clients c ON td.clientID = c.clientID;
        """
        cur = mysql.connection.cursor()
        cur.execute(query)
        trackeddays = cur.fetchall()

    # Fetch all client names for autocomplete
    query = "SELECT clientName FROM Clients;"
    cur.execute(query)
    clients = cur.fetchall()

    return render_template("trackeddays.j2", trackeddays=trackeddays, clients=clients)

@app.route('/foods')
def foods():
    query = "SELECT * FROM Foods;"
    cur = mysql.connection.cursor()
    cur.execute(query)
    foods = cur.fetchall()
    return render_template("foods.j2", foods=foods)

@app.route('/foodentries')
def foodentries():
    query = """
    SELECT 
        FoodEntries.foodEntryID, 
        TrackedDays.trackedDayDate, 
        Clients.clientName, 
        Foods.foodName, 
        FoodEntries.foodEntryCalories, 
        FoodEntries.foodEntryGramWeight, 
        FoodEntries.foodEntryNote
    FROM 
        FoodEntries
    JOIN 
        Foods ON FoodEntries.foodID = Foods.foodID
    JOIN 
        TrackedDays ON FoodEntries.trackedDayID = TrackedDays.trackedDayID
    JOIN 
        Clients ON TrackedDays.clientID = Clients.clientID;
    """
    cur = mysql.connection.cursor()
    cur.execute(query)
    foodentries = cur.fetchall()
    return render_template("foodentries.j2", foodentries=foodentries)

@app.route('/exerciseentries')
def exerciseentries():
    query = """
    SELECT 
        ExerciseEntries.exerciseEntryID, 
        TrackedDays.trackedDayDate, 
        Clients.clientName, 
        ExerciseEntries.exerciseEntryName, 
        ExerciseEntries.exerciseEntryType, 
        ExerciseEntries.exerciseEntryCalories, 
        ExerciseEntries.exerciseEntryNote
    FROM 
        ExerciseEntries
    JOIN 
        TrackedDays ON ExerciseEntries.trackedDayID = TrackedDays.trackedDayID
    JOIN 
        Clients ON TrackedDays.clientID = Clients.clientID;
    """
    cur = mysql.connection.cursor()
    cur.execute(query)
    exerciseentries = cur.fetchall()
    return render_template("exerciseentries.j2", exerciseentries=exerciseentries)

# Listener
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 15834)) 
    app.run(port=port, debug=True)