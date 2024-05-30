"""
Citation for the following code:
Date: 29/05/2024
Authors: Rami Albaroudi and Mohamed Saud, Group 13
Adapted from https://github.com/osu-cs340-ecampus/flask-starter-app with significant modifications
"""

# Imports
from flask import Flask, render_template, request, redirect, json
from flask_mysqldb import MySQL
from MySQLdb import IntegrityError
import os
import database.db_connector as db
import re
from email_validator import validate_email, EmailNotValidError

# Configure connection to the database
app = Flask(__name__)
app.config["MYSQL_HOST"] = db.host
app.config["MYSQL_USER"] = db.user
app.config["MYSQL_PASSWORD"] = db.passwd
app.config["MYSQL_DB"] = db.db
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
mysql = MySQL(app)

""" -------- Routes for Home -------- """


# We want / and /index to lead to the same place.
@app.route("/")
@app.route("/index")
def index():
    # We use Jinja/Flask templates to build the foundation for our pages
    return render_template("index.j2")


""" -------- Routes for Staff -------- """


# Route for Reading and Updating Staff Records
@app.route("/staff", methods=["GET", "POST"])
def staff():
    if request.method == "POST":
        staffName = request.form["staffName"]
        staffEmail = request.form["staffEmail"]
        staffCapacity = request.form["staffCapacity"]
        staffNote = request.form["staffNote"]
        # We check for errors by calling the validateStaffForm helper function to make sure the data is okay before we pass it to the DB
        errors = validateStaffForm(staffName, staffEmail)
        if not errors:
            # This is the Python equivalent of try/catch in JS
            try:
                # Validate the email address
                validate_email(staffEmail)
                insertStaff(staffName, staffEmail, staffCapacity, staffNote)
                return redirect("/staff")
            # We use the email not valid error from the email_validator module in order to raise an error if a user's email is invalid.
            except EmailNotValidError:
                return "Invalid email.", 400
            # We use the integrity error module in order to raise an error if a user's query would crash the database.
            except IntegrityError:
                return "A staff member with this email already exists.", 400
        return render_template("staff.j2", staff=fetchStaff(), errors=errors)
    return render_template("staff.j2", staff=fetchStaff())


# Route for Updating Staff Records
@app.route("/updatestaff/<int:staffID>", methods=["POST"])
def updateStaff(staffID):
    staffName = request.form["staffName"]
    staffEmail = request.form["staffEmail"]
    staffCapacity = request.form["staffCapacity"]
    staffNote = request.form["staffNote"]
    errors = validateStaffForm(staffName, staffEmail)
    if not errors:
        try:
            validate_email(staffEmail)
            updateStaffRecord(staffID, staffName, staffEmail, staffCapacity, staffNote)
            return "OK"
        except EmailNotValidError:
            errors.append("Invalid email.")
        except IntegrityError:
            errors.append("A staff member with this email already exists.")
    return ", ".join(errors), 400


# Route for Deleting Staff Records
@app.route("/deletestaff/<int:staffID>", methods=["POST"])
def deleteStaff(staffID):
    deleteStaffRecord(staffID)
    return redirect("/staff")


# Helper function for validation for the Staff Form
def validateStaffForm(staffName, staffEmail):
    errors = []
    if not staffName:
        errors.append("Name is required.")
    if not staffEmail:
        errors.append("Email is required.")
    return errors


# Helper function to READ the Staff Records
def fetchStaff():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Staff;")
    return cur.fetchall()


# Helper function to CREATE a Staff Record
def insertStaff(staffName, staffEmail, staffCapacity, staffNote):
    cur = mysql.connection.cursor()
    try:
        # Our query placeholders are slightly different from the DML file due to Python/Flask requirements. This also helps prevent SQL injection
        validate_email(staffEmail)
        cur.execute(
            "INSERT INTO Staff (staffName, staffEmail, staffCapacity, staffNote) VALUES (%s, %s, %s, %s);",
            (staffName, staffEmail, staffCapacity, staffNote),
        )
        # This is how we send the data to the DB
        mysql.connection.commit()
    except EmailNotValidError as e:
        # We use this to roll back the change if there was an error with the query
        mysql.connection.rollback()
        raise e
    except IntegrityError as e:
        # We use this to roll back the change if there was an error with the query
        mysql.connection.rollback()
        raise e


# Helper function to UPDATE a Staff Record
def updateStaffRecord(staffID, staffName, staffEmail, staffCapacity, staffNote):
    cur = mysql.connection.cursor()
    try:
        validate_email(staffEmail)
        cur.execute(
            "UPDATE Staff SET staffName = %s, staffEmail = %s, staffCapacity = %s, staffNote = %s WHERE staffID = %s;",
            (staffName, staffEmail, staffCapacity, staffNote, staffID),
        )
        mysql.connection.commit()
    except EmailNotValidError as e:
        # We use this to roll back the change if there was an error with the query
        mysql.connection.rollback()
        raise e
    except IntegrityError as e:
        mysql.connection.rollback()
        raise e


# Helper function to DELETE a Staff record
def deleteStaffRecord(staffID):
    cur = mysql.connection.cursor()
    # We don't need validation here because DELETE is pretty simple
    cur.execute("DELETE FROM Staff WHERE staffID = %s;", (staffID,))
    mysql.connection.commit()


""" -------- Routes for Clients -------- """


# Route for Reading and Updating Client Records
@app.route("/clients", methods=["GET", "POST"])
def clients():
    if request.method == "POST":
        clientName = request.form["clientName"]
        clientEmail = request.form["clientEmail"]
        clientSex = request.form["clientSex"]
        clientAge = request.form["clientAge"]
        clientHeight = request.form["clientHeight"]
        clientWeight = request.form["clientWeight"]
        clientActivityLevel = request.form["clientActivityLevel"]
        clientCalorieTarget = request.form["clientCalorieTarget"]
        clientNote = request.form["clientNote"]
        # We check for errors by calling the validateClientForm helper function to make sure the data is okay before we pass it to the DB
        errors = validateClientForm(
            clientName,
            clientEmail,
            clientAge,
            clientHeight,
            clientWeight,
            clientCalorieTarget,
        )
        if not errors:
            try:
                # Validate the email address
                validate_email(clientEmail)
                insertClient(
                    clientName,
                    clientEmail,
                    clientSex,
                    clientAge,
                    clientHeight,
                    clientWeight,
                    clientActivityLevel,
                    clientCalorieTarget,
                    clientNote,
                )
                return redirect("/clients")
            except EmailNotValidError:
                return "Invalid email.", 400
            except IntegrityError:
                return "A client with this email already exists.", 400
        return render_template("clients.j2", clients=fetchClients(), errors=errors)
    return render_template("clients.j2", clients=fetchClients())


# Route for Updating Client Records
@app.route("/updateclient/<int:clientID>", methods=["POST"])
def updateClient(clientID):
    clientName = request.form["clientName"]
    clientEmail = request.form["clientEmail"]
    clientSex = request.form["clientSex"]
    clientAge = request.form["clientAge"]
    clientHeight = request.form["clientHeight"]
    clientWeight = request.form["clientWeight"]
    clientActivityLevel = request.form["clientActivityLevel"]
    clientCalorieTarget = request.form["clientCalorieTarget"]
    clientNote = request.form["clientNote"]
    errors = validateClientForm(
        clientName,
        clientEmail,
        clientAge,
        clientHeight,
        clientWeight,
        clientCalorieTarget,
    )
    if not errors:
        try:
            validate_email(clientEmail)
            updateClientRecord(
                clientID,
                clientName,
                clientEmail,
                clientSex,
                clientAge,
                clientHeight,
                clientWeight,
                clientActivityLevel,
                clientCalorieTarget,
                clientNote,
            )
            return "OK"
        except EmailNotValidError:
            errors.append("Invalid email.")
        except IntegrityError:
            errors.append("A client with this email already exists.")
    return ", ".join(errors), 400


# Route for Deleting Client Records
@app.route("/deleteclient/<int:clientID>", methods=["POST"])
def deleteClient(clientID):
    deleteClientRecord(clientID)
    return redirect("/clients")


# Helper function for validation for the Client Form
def validateClientForm(
    clientName, clientEmail, clientAge, clientHeight, clientWeight, clientCalorieTarget
):
    errors = []
    if not clientName:
        errors.append("Name is required.")
    if not clientEmail:
        errors.append("Email is required.")
    if not clientAge or int(clientAge) < 1:
        errors.append("Invalid age. Must be greater than 0.")
    if not clientHeight or float(clientHeight) <= 0:
        errors.append("Invalid height. Must be greater than 0.")
    if not clientWeight or float(clientWeight) <= 0:
        errors.append("Invalid weight. Must be greater than 0.")
    if not clientCalorieTarget or int(clientCalorieTarget) <= 0:
        errors.append("Invalid calorie target. Must be greater than 0.")
    return errors


# Helper function to READ the Client Records
def fetchClients():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Clients;")
    return cur.fetchall()


# Helper function to CREATE a Client Record
def insertClient(
    clientName,
    clientEmail,
    clientSex,
    clientAge,
    clientHeight,
    clientWeight,
    clientActivityLevel,
    clientCalorieTarget,
    clientNote,
):
    cur = mysql.connection.cursor()
    try:
        validate_email(clientEmail)
        cur.execute(
            "INSERT INTO Clients (clientName, clientEmail, clientSex, clientAge, clientHeight, clientWeight, clientActivityLevel, clientCalorieTarget, clientNote) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);",
            (
                clientName,
                clientEmail,
                clientSex,
                clientAge,
                clientHeight,
                clientWeight,
                clientActivityLevel,
                clientCalorieTarget,
                clientNote,
            ),
        )
        mysql.connection.commit()
    except EmailNotValidError as e:
        mysql.connection.rollback()
        raise e
    except IntegrityError as e:
        mysql.connection.rollback()
        raise e


# Helper function to UPDATE a Client Record
def updateClientRecord(
    clientID,
    clientName,
    clientEmail,
    clientSex,
    clientAge,
    clientHeight,
    clientWeight,
    clientActivityLevel,
    clientCalorieTarget,
    clientNote,
):
    cur = mysql.connection.cursor()
    try:
        validate_email(clientEmail)
        cur.execute(
            "UPDATE Clients SET clientName = %s, clientEmail = %s, clientSex = %s, clientAge = %s, clientHeight = %s, clientWeight = %s, clientActivityLevel = %s, clientCalorieTarget = %s, clientNote = %s WHERE clientID = %s;",
            (
                clientName,
                clientEmail,
                clientSex,
                clientAge,
                clientHeight,
                clientWeight,
                clientActivityLevel,
                clientCalorieTarget,
                clientNote,
                clientID,
            ),
        )
        mysql.connection.commit()
    except EmailNotValidError as e:
        mysql.connection.rollback()
        raise e
    except IntegrityError as e:
        mysql.connection.rollback()
        raise e


# Helper function to DELETE a Client record
def deleteClientRecord(clientID):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Clients WHERE clientID = %s;", (clientID,))
    mysql.connection.commit()


""" -------- Routes for Staff-Client Assignments -------- """


# Route for Reading and Updating Staff-Client Assignments
@app.route("/staffclients", methods=["GET", "POST"])
def staffclients():
    if request.method == "POST":
        staffName = request.form["searchStaff"]
        clientName = request.form["searchClient"]
        staffID = getStaffByName(staffName)
        clientID = getClientByName(clientName)
        if staffID and clientID:
            try:
                addStaffClientRecord(staffID, clientID)
                return redirect("/staffclients")
            except IntegrityError:
                return "Assignment already exists.", 400
        else:
            return "Invalid staff or client name.", 400
    return render_template(
        "staffclients.j2",
        staffclients=fetchStaffClients(),
        staff=fetchStaff(),
        clients=fetchClients(),
    )


# Route for Updating Staff-Client Assignments
@app.route("/updatestaffclient/<int:staffID>/<int:clientID>", methods=["POST"])
def updateStaffClient(staffID, clientID):
    staffName = request.form["staffName"]
    clientName = request.form["clientName"]
    newStaffID = getStaffByName(staffName)
    newClientID = getClientByName(clientName)
    if newStaffID and newClientID:
        try:
            updateStaffClientRecord(staffID, clientID, newStaffID, newClientID)
            return "OK"
        except IntegrityError:
            return "Failed to update record.", 400
    else:
        return "Invalid staff or client name.", 400


# Route for Deleting Staff-Client Assignments
@app.route("/deletestaffclient/<int:staffID>/<int:clientID>", methods=["POST"])
def deleteStaffClient(staffID, clientID):
    deleteStaffClientRecord(staffID, clientID)
    return redirect("/staffclients")


# Helper function to READ Staff-Client Assignments
def fetchStaffClients():
    cur = mysql.connection.cursor()
    query = """
    SELECT sc.staffID, s.staffName, sc.clientID, c.clientName
    FROM StaffClients sc
    JOIN Staff s ON sc.staffID = s.staffID
    JOIN Clients c ON sc.clientID = c.clientID;
    """
    cur.execute(query)
    return cur.fetchall()


# Helper function to READ Staff Records
def fetchStaff():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Staff;")
    return cur.fetchall()


# Helper function to READ Client Records
def fetchClients():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Clients;")
    return cur.fetchall()


# Helper function to get Staff ID by Name
def getStaffByName(staffName):
    cur = mysql.connection.cursor()
    cur.execute("SELECT staffID FROM Staff WHERE staffName = %s;", (staffName,))
    result = cur.fetchone()
    return result["staffID"] if result else None


# Helper function to get Client ID by Name
def getClientByName(clientName):
    cur = mysql.connection.cursor()
    cur.execute("SELECT clientID FROM Clients WHERE clientName = %s;", (clientName,))
    result = cur.fetchone()
    return result["clientID"] if result else None


# Helper function to CREATE a Staff-Client Assignment
def addStaffClientRecord(staffID, clientID):
    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO StaffClients (staffID, clientID) VALUES (%s, %s);",
        (staffID, clientID),
    )
    mysql.connection.commit()


# Helper function to UPDATE a Staff-Client Assignment
def updateStaffClientRecord(staffID, clientID, newStaffID, newClientID):
    cur = mysql.connection.cursor()
    cur.execute(
        "UPDATE StaffClients SET staffID = %s, clientID = %s WHERE staffID = %s AND clientID = %s;",
        (newStaffID, newClientID, staffID, clientID),
    )
    mysql.connection.commit()


# Helper function to DELETE a Staff-Client Assignment
def deleteStaffClientRecord(staffID, clientID):
    cur = mysql.connection.cursor()
    cur.execute(
        "DELETE FROM StaffClients WHERE staffID = %s AND clientID = %s;",
        (staffID, clientID),
    )
    mysql.connection.commit()


""" -------- Routes for Tracked Days -------- """


# TODO: Implement CUD
@app.route("/trackeddays", methods=["GET", "POST"])
def trackeddays():
    if request.method == "POST":
        search_query = request.form["search_query"]
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
        cur.execute(query, ("%" + search_query + "%",))
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

    # Get all client names for autocomplete
    query = "SELECT clientName FROM Clients;"
    cur.execute(query)
    clients = cur.fetchall()

    return render_template("trackeddays.j2", trackeddays=trackeddays, clients=clients)


""" -------- Routes for Foods -------- """


# Route for Reading and Updating Food Records
@app.route("/foods", methods=["GET", "POST"])
def foods():
    if request.method == "POST":
        foodName = request.form["foodName"]
        foodType = request.form["foodType"]
        foodCaloriesPerGram = request.form["foodCaloriesPerGram"]
        foodNote = request.form["foodNote"]
        # We check for errors by calling the validateFoodForm helper function to make sure the data is okay before we pass it to the DB
        errors = validateFoodForm(foodName, foodType, foodCaloriesPerGram)
        if not errors:
            try:
                insertFood(foodName, foodType, foodCaloriesPerGram, foodNote)
                return redirect("/foods")
            except IntegrityError:
                return "A food with this name already exists.", 400
        return render_template("foods.j2", foods=fetchFoods(), errors=errors)
    return render_template("foods.j2", foods=fetchFoods())


# Route for Updating Food Records
@app.route("/updatefood/<int:foodID>", methods=["POST"])
def updateFood(foodID):
    foodName = request.form["foodName"]
    foodType = request.form["foodType"]
    foodCaloriesPerGram = request.form["foodCaloriesPerGram"]
    foodNote = request.form["foodNote"]
    errors = validateFoodForm(foodName, foodType, foodCaloriesPerGram)
    if not errors:
        try:
            updateFoodRecord(foodID, foodName, foodType, foodCaloriesPerGram, foodNote)
            return "OK"
        except IntegrityError:
            errors.append("A food with this name already exists.")
    return ", ".join(errors), 400


# Route for Deleting Food Records
@app.route("/deletefood/<int:foodID>", methods=["POST"])
def deleteFood(foodID):
    deleteFoodRecord(foodID)
    return redirect("/foods")


# Helper function for validation for the Food Form
def validateFoodForm(foodName, foodType, foodCaloriesPerGram):
    errors = []
    if not foodName:
        errors.append("Name is required.")
    if not foodType:
        errors.append("Type is required.")
    if not foodCaloriesPerGram:
        errors.append("Calories per gram is required.")
    elif float(foodCaloriesPerGram) < 0.01:
        errors.append("Calories per gram cannot be less than 0.01.")
    return errors


# Helper function to READ the Food Records
def fetchFoods():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Foods;")
    return cur.fetchall()


# Helper function to CREATE a Food Record
def insertFood(foodName, foodType, foodCaloriesPerGram, foodNote):
    cur = mysql.connection.cursor()
    try:
        cur.execute(
            "INSERT INTO Foods (foodName, foodType, foodCaloriesPerGram, foodNote) VALUES (%s, %s, %s, %s);",
            (foodName, foodType, foodCaloriesPerGram, foodNote),
        )
        mysql.connection.commit()
    except IntegrityError as e:
        mysql.connection.rollback()
        raise e


# Helper function to UPDATE a Food Record
def updateFoodRecord(foodID, foodName, foodType, foodCaloriesPerGram, foodNote):
    cur = mysql.connection.cursor()
    try:
        cur.execute(
            "UPDATE Foods SET foodName = %s, foodType = %s, foodCaloriesPerGram = %s, foodNote = %s WHERE foodID = %s;",
            (foodName, foodType, foodCaloriesPerGram, foodNote, foodID),
        )
        mysql.connection.commit()
    except IntegrityError as e:
        mysql.connection.rollback()
        raise e


# Helper function to DELETE a Food record
def deleteFoodRecord(foodID):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM Foods WHERE foodID = %s;", (foodID,))
    mysql.connection.commit()


""" -------- Routes for Food Entries -------- """


# TODO: Implement CUD
@app.route("/foodentries")
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
    LEFT JOIN 
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


""" -------- Routes for Exercise Entries -------- """


# TODO: Implement CUD
@app.route("/exerciseentries")
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
    port = int(os.environ.get("PORT", 15834))
    app.run(port=port, debug=True)
