"""
Citation for the following code:
Date: 06/06/2024
Authors: Rami Albaroudi and Mohamed Saud, Group 13
Copied from https://github.com/osu-cs340-ecampus/flask-starter-app with minor modifications
"""

""" ___________ Imports List ___________ """
from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
# IntegrityError is used to check if a query would create an error in the DB
from MySQLdb import IntegrityError
import os
import database.db_connector as db
# email_validator is used to check if email inputs are valid without needing to
# manually check using regex or other methods
from email_validator import validate_email, EmailNotValidError

""" ___________ Database Connection/Configuration ___________ """
app = Flask(__name__)
app.config["MYSQL_HOST"] = db.host
app.config["MYSQL_USER"] = db.user
app.config["MYSQL_PASSWORD"] = db.passwd
app.config["MYSQL_DB"] = db.db
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
mysql = MySQL(app)

"""
Citation for the following code:
Date: 06/06/2024
Authors: Rami Albaroudi and Mohamed Saud, Group 13
Primarily original work, some code snippets/starter code adapted from
https://github.com/osu-cs340-ecampus/flask-starter-app with significant modifications
"""

""" ___________ Routes for Home/Index Page ___________ """
# We want / and /index to lead to the same place.
@app.route("/")
@app.route("/index")
def index():
    # We use Jinja/Flask templates to build the foundation for our pages
    return render_template("index.j2")

""" ___________ Routes for Staff Page ___________ """
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
            # We use the integrity error module in order to raise an error if a user's query would cause an error in the database, like a duplicate entry or an invalid null value
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
        # Then raise the error message 
        raise e
    except IntegrityError as e:
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
    # We don't need to call the validator function here because DELETE is pretty simple
    cur.execute("DELETE FROM Staff WHERE staffID = %s;", (staffID,))
    mysql.connection.commit()

""" ___________ Routes for Clients Page ___________ """
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
            # Check for invalid emails
            except EmailNotValidError:
                return "Invalid email.", 400
            # Check for possible data integrity errors
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

""" ___________ Routes for Staff-Client Assignments Page ___________ """
# Route for Reading and Updating Staff-Client Assignments
@app.route("/staffclients", methods=["GET", "POST"])
def staffclients():
    if request.method == "POST":
        staffName = request.form["searchStaff"]
        clientName = request.form["searchClient"]
        # Retrieve staff and client names to make using the form easier
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
        clients=fetchClientsAssignments(),
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
def fetchClientsAssignments():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Clients;")
    return cur.fetchall()

# Helper function to get Staff ID by Name since the users will enter names and not IDs
def getStaffByName(staffName):
    cur = mysql.connection.cursor()
    cur.execute("SELECT staffID FROM Staff WHERE staffName = %s;", (staffName,))
    result = cur.fetchone()
    return result["staffID"] if result else None

# Helper function to get Client ID by Name since the users will enter names and not IDs
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

""" ___________ Routes for Tracked Days Page ___________ """
# Route for Reading and Creating Tracked Days
@app.route("/trackeddays", methods=["GET", "POST"])
def trackeddays():
    if request.method == "POST":
        clientName = request.form.get("clientName")
        trackedDayDate = request.form.get("trackedDayDate")
        trackedDayCalorieTarget = request.form.get("trackedDayCalorieTarget")
        trackedDayNote = request.form.get("trackedDayNote")
        # Fetch the client ID based on the client name
        clientID = getClientNameDays(clientName)
        if not clientID:
            return "Client not found.", 400
        # Validate the form inputs
        errors = validateTrackedDayForm(
            clientID, trackedDayDate, trackedDayCalorieTarget
        )
        if not errors:
            try:
                insertTrackedDay(
                    clientID, trackedDayDate, trackedDayCalorieTarget, trackedDayNote
                )
                return redirect("/trackeddays")
            except IntegrityError:
                return "Error inserting tracked day.", 400
        return render_template(
            "trackeddays.j2",
            trackeddays=fetchTrackedDays(),
            clients=fetchClientsDays(),
            errors=errors,
        )
    else:
        return render_template(
            "trackeddays.j2", trackeddays=fetchTrackedDays(), clients=fetchClientsDays()
        )

# Tie the entered client name back to the client ID for the search boxes
def getClientNameDays(clientName):
    query = "SELECT clientID FROM Clients WHERE clientName = %s;"
    cur = mysql.connection.cursor()
    cur.execute(query, (clientName,))
    result = cur.fetchone()
    return result["clientID"] if result else None

# Route for Updating Tracked Days
@app.route("/updatetrackedday/<int:trackedDayID>", methods=["POST"])
def updateTrackedDay(trackedDayID):
    clientID = request.form.get("clientID")
    trackedDayDate = request.form.get("trackedDayDate")
    trackedDayCalorieTarget = request.form.get("trackedDayCalorieTarget")
    trackedDayNote = request.form.get("trackedDayNote")
    # Validate the form inputs
    errors = validateTrackedDayForm(clientID, trackedDayDate, trackedDayCalorieTarget)
    if not errors:
        try:
            updateTrackedDayRecord(
                trackedDayID,
                clientID,
                trackedDayDate,
                trackedDayCalorieTarget,
                trackedDayNote,
            )
            return "OK"
        except IntegrityError:
            return "Error updating tracked day.", 400
    return ", ".join(errors), 400

# Route for Deleting Tracked Days
@app.route("/deletetrackedday/<int:trackedDayID>", methods=["POST"])
def deleteTrackedDay(trackedDayID):
    deleteTrackedDayRecord(trackedDayID)
    return redirect("/trackeddays")

# Helper function for validation for the Tracked Day Form
def validateTrackedDayForm(clientID, trackedDayDate, trackedDayCalorieTarget):
    errors = []
    if not clientID:
        errors.append("Client ID is required.")
    if not trackedDayDate:
        errors.append("Date is required.")
    if not trackedDayCalorieTarget:
        errors.append("Calorie target is required.")
    elif int(trackedDayCalorieTarget) < 1:
        errors.append("Calorie target must be at least 1.")
    return errors

# Helper function to CREATE a Tracked Day Record
def insertTrackedDay(clientID, trackedDayDate, trackedDayCalorieTarget, trackedDayNote):
    cur = mysql.connection.cursor()
    try:
        cur.execute(
            "INSERT INTO TrackedDays (clientID, trackedDayDate, trackedDayCalorieTarget, trackedDayNote) VALUES (%s, %s, %s, %s);",
            (clientID, trackedDayDate, trackedDayCalorieTarget, trackedDayNote),
        )
        mysql.connection.commit()
    except IntegrityError as e:
        mysql.connection.rollback()
        raise e

# Helper function to UPDATE a Tracked Day Record
def updateTrackedDayRecord(
    trackedDayID, clientID, trackedDayDate, trackedDayCalorieTarget, trackedDayNote
):
    cur = mysql.connection.cursor()
    try:
        query = """
        UPDATE TrackedDays 
        SET clientID = %s, trackedDayDate = %s, trackedDayCalorieTarget = %s, trackedDayNote = %s 
        WHERE trackedDayID = %s;
        """
        cur.execute(
            query,
            (
                clientID,
                trackedDayDate,
                trackedDayCalorieTarget,
                trackedDayNote,
                trackedDayID,
            ),
        )
        mysql.connection.commit()
    except IntegrityError as e:
        mysql.connection.rollback()
        print(f"IntegrityError: {e}")
        raise e

# Helper function to DELETE a Tracked Day Record
def deleteTrackedDayRecord(trackedDayID):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM TrackedDays WHERE trackedDayID = %s;", (trackedDayID,))
    mysql.connection.commit()

# Helper function to READ the Tracked Days Records
def fetchTrackedDays():
    cur = mysql.connection.cursor()
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
    cur.execute(query)
    return cur.fetchall()

# Helper function to READ the Clients Records
def fetchClientsDays():
    cur = mysql.connection.cursor()
    cur.execute("SELECT clientID, clientName FROM Clients;")
    return cur.fetchall()

""" ___________ Routes for Foods Page ___________ """
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

""" ___________ Routes for Food Entries Page ___________ """
# Route for displaying Food Entries
@app.route("/foodentries", methods=["GET"])
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
    return render_template(
        "foodentries.j2",
        foodentries=foodentries,
        clients=fetchClientNamesFoodEntries(),
        foods=fetchFoodNames(),
    )

# Route for adding food entries
@app.route("/addfoodentry", methods=["POST"])
def addfoodentry():
    trackedDayDate = request.form["trackedDayDate"]
    clientName = request.form["clientName"]
    foodName = request.form["foodName"]
    gramWeight = request.form["gramWeight"]
    calories = request.form["calories"]
    note = request.form["note"]
    # Fetch the tracked day ID since tracked days are an FK inside food entries
    trackedDayID = getTrackedDayFoodEntries(trackedDayDate, clientName)
    if not trackedDayID:
        return "Tracked day not found for the given date and client name.", 400
    # Fetch the food ID if there is one, otherwise set it to NULL (Foods are Nullable in Food Entries)
    foodID = fetchFoodsFoodEntries(foodName)
    if not foodID:
        foodID = None
    cur = mysql.connection.cursor()
    try:
        cur.execute(
            "INSERT INTO FoodEntries (trackedDayID, foodID, foodEntryCalories, foodEntryGramWeight, foodEntryNote) VALUES (%s, %s, %s, %s, %s);",
            (trackedDayID, foodID, calories, gramWeight, note),
        )
        mysql.connection.commit()
        return redirect("/foodentries")
    except IntegrityError:
        mysql.connection.rollback()
        return "An error occurred while adding the food entry.", 400

# Route for updating food entries
@app.route("/updatefoodentry/<int:foodEntryID>", methods=["POST"])
def updatefoodentry(foodEntryID):
    gramWeight = request.form["gramWeight"]
    calories = request.form["calories"]
    note = request.form["note"]
    # Validate the input values
    if not gramWeight or int(gramWeight) < 1:
        return "Weight must be at least 1 gram.", 400
    if not calories or int(calories) < 1:
        return "Calories must be at least 1.", 400
    cur = mysql.connection.cursor()
    try:
        cur.execute(
            "UPDATE FoodEntries SET foodEntryCalories = %s, foodEntryGramWeight = %s, foodEntryNote = %s WHERE foodEntryID = %s;",
            (calories, gramWeight, note, foodEntryID),
        )
        mysql.connection.commit()
        return "OK"
    except IntegrityError:
        mysql.connection.rollback()
        return "An error occurred while updating the food entry.", 400

# Route for setting a Food Name to NULL in a Food Entry, since the relationship is nullable
@app.route("/setfoodnull/<int:foodEntryID>", methods=["POST"])
def setfoodnull(foodEntryID):
    cur = mysql.connection.cursor()
    try:
        cur.execute(
            "UPDATE FoodEntries SET foodID = NULL WHERE foodEntryID = %s;",
            (foodEntryID,),
        )
        mysql.connection.commit()
        return "OK"
    except IntegrityError:
        mysql.connection.rollback()
        return "An error occurred while removing the food entry.", 400

# Route for deleting Food Entries
@app.route("/deletefoodentry/<int:foodEntryID>", methods=["POST"])
def deletefoodentry(foodEntryID):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM FoodEntries WHERE foodEntryID = %s;", (foodEntryID,))
    mysql.connection.commit()
    return redirect("/foodentries")

# Route to retrieved the tracked day associated with a food entry using the client name and date
def getTrackedDayFoodEntries(trackedDayDate, clientName):
    query = """
    SELECT TrackedDays.trackedDayID
    FROM TrackedDays
    JOIN Clients ON TrackedDays.clientID = Clients.clientID
    WHERE TrackedDays.trackedDayDate = %s AND Clients.clientName = %s;
    """
    cur = mysql.connection.cursor()
    cur.execute(query, (trackedDayDate, clientName))
    result = cur.fetchone()
    return result["trackedDayID"] if result else None

# Route to get the food ID using the food name
def fetchFoodsFoodEntries(foodName):
    query = "SELECT foodID FROM Foods WHERE foodName = %s;"
    cur = mysql.connection.cursor()
    cur.execute(query, (foodName,))
    result = cur.fetchone()
    return result["foodID"] if result else None

# Route to get Client Names 
def fetchClientNamesFoodEntries():
    query = "SELECT clientName FROM Clients;"
    cur = mysql.connection.cursor()
    cur.execute(query)
    return cur.fetchall()

# Route to get Food Names
def fetchFoodNames():
    query = "SELECT foodName FROM Foods;"
    cur = mysql.connection.cursor()
    cur.execute(query)
    return cur.fetchall()

""" ___________ Routes for Exercise Entries Page ___________ """
# Route for Reading and Creating Exercise Entries
@app.route("/exerciseentries", methods=["GET", "POST"])
def exerciseentries():
    if request.method == "POST":
        trackedDayDate = request.form["trackedDayDate"]
        clientName = request.form["clientName"]
        exerciseEntryName = request.form["exerciseName"]
        exerciseEntryType = request.form["type"]
        exerciseEntryCalories = request.form["calories"]
        exerciseEntryNote = request.form["note"]
        # Fetch the tracked day ID
        trackedDayID = getTrackedDaysExerciseEntries(trackedDayDate, clientName)
        if not trackedDayID:
            return "Tracked day not found for the given date and client name.", 400
        # Validate the form data
        errors = validateExerciseEntryForm(
            exerciseEntryName, exerciseEntryType, exerciseEntryCalories
        )
        if not errors:
            try:
                insertExerciseEntry(
                    trackedDayID,
                    exerciseEntryName,
                    exerciseEntryType,
                    exerciseEntryCalories,
                    exerciseEntryNote,
                )
                return redirect("/exerciseentries")
            except IntegrityError:
                return "An error occurred while adding the exercise entry.", 400
        return render_template(
            "exerciseentries.j2",
            exerciseentries=fetchExerciseEntries(),
            errors=errors,
            clients=fetchClientNamesFoodEntries(),
        )
    return render_template(
        "exerciseentries.j2",
        exerciseentries=fetchExerciseEntries(),
        clients=fetchClientNamesExerciseEntries(),
    )

# Route for Updating Exercise Entries
@app.route("/updateexerciseentry/<int:exerciseEntryID>", methods=["POST"])
def updateExerciseEntry(exerciseEntryID):
    exerciseEntryName = request.form["exerciseEntryName"]
    exerciseEntryType = request.form["exerciseEntryType"]
    exerciseEntryCalories = request.form["exerciseEntryCalories"]
    exerciseEntryNote = request.form["exerciseEntryNote"]
    # Validate the form data
    errors = validateExerciseEntryForm(
        exerciseEntryName, exerciseEntryType, exerciseEntryCalories
    )
    if not errors:
        try:
            updateExerciseEntryRecord(
                exerciseEntryID,
                exerciseEntryName,
                exerciseEntryType,
                exerciseEntryCalories,
                exerciseEntryNote,
            )
            return "OK"
        except IntegrityError:
            errors.append("An error occurred while updating the exercise entry.")
    return ", ".join(errors), 400

# Route for Deleting Exercise Entries
@app.route("/deleteexerciseentry/<int:exerciseEntryID>", methods=["POST"])
def deleteExerciseEntry(exerciseEntryID):
    deleteExerciseEntryRecord(exerciseEntryID)
    return redirect("/exerciseentries")

# Helper function for validation for the Exercise Entry Form
def validateExerciseEntryForm(
    exerciseEntryName, exerciseEntryType, exerciseEntryCalories
):
    errors = []
    if not exerciseEntryName:
        errors.append("Exercise name is required.")
    if not exerciseEntryType:
        errors.append("Exercise type is required.")
    if not exerciseEntryCalories or int(exerciseEntryCalories) <= 0:
        errors.append("Calories must be a positive number.")
    return errors

# Helper function to READ the Exercise Entries
def fetchExerciseEntries():
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
    return cur.fetchall()

# Helper function to CREATE an Exercise Entry
def insertExerciseEntry(
    trackedDayID,
    exerciseEntryName,
    exerciseEntryType,
    exerciseEntryCalories,
    exerciseEntryNote,
):
    cur = mysql.connection.cursor()
    try:
        cur.execute(
            "INSERT INTO ExerciseEntries (trackedDayID, exerciseEntryName, exerciseEntryType, exerciseEntryCalories, exerciseEntryNote) VALUES (%s, %s, %s, %s, %s);",
            (
                trackedDayID,
                exerciseEntryName,
                exerciseEntryType,
                exerciseEntryCalories,
                exerciseEntryNote,
            ),
        )
        mysql.connection.commit()
    except IntegrityError as e:
        mysql.connection.rollback()
        raise e

# Helper function to UPDATE an Exercise Entry
def updateExerciseEntryRecord(
    exerciseEntryID,
    exerciseEntryName,
    exerciseEntryType,
    exerciseEntryCalories,
    exerciseEntryNote,
):
    cur = mysql.connection.cursor()
    try:
        cur.execute(
            "UPDATE ExerciseEntries SET exerciseEntryName = %s, exerciseEntryType = %s, exerciseEntryCalories = %s, exerciseEntryNote = %s WHERE exerciseEntryID = %s;",
            (
                exerciseEntryName,
                exerciseEntryType,
                exerciseEntryCalories,
                exerciseEntryNote,
                exerciseEntryID,
            ),
        )
        mysql.connection.commit()
    except IntegrityError as e:
        mysql.connection.rollback()
        raise e

# Helper function to DELETE an Exercise Entry
def deleteExerciseEntryRecord(exerciseEntryID):
    cur = mysql.connection.cursor()
    cur.execute(
        "DELETE FROM ExerciseEntries WHERE exerciseEntryID = %s;", (exerciseEntryID,)
    )
    mysql.connection.commit()

# Helper function to fetch client names and tracked day dates
def fetchClientNamesAndTrackedDays():
    query = """
    SELECT 
        Clients.clientID, 
        Clients.clientName, 
        TrackedDays.trackedDayID, 
        TrackedDays.trackedDayDate
    FROM 
        Clients
    JOIN 
        TrackedDays ON Clients.clientID = TrackedDays.clientID;
    """
    cur = mysql.connection.cursor()
    cur.execute(query)
    return cur.fetchall()

# Route to get the tracked dayy ID using the date and client name
def getTrackedDaysExerciseEntries(trackedDayDate, clientName):
    query = """
    SELECT TrackedDays.trackedDayID
    FROM TrackedDays
    JOIN Clients ON TrackedDays.clientID = Clients.clientID
    WHERE TrackedDays.trackedDayDate = %s AND Clients.clientName = %s;
    """
    cur = mysql.connection.cursor()
    cur.execute(query, (trackedDayDate, clientName))
    result = cur.fetchone()
    return result["trackedDayID"] if result else None

# Route to get the client names and IDs
def fetchClientNamesExerciseEntries():
    query = "SELECT clientID, clientName FROM Clients;"
    cur = mysql.connection.cursor()
    cur.execute(query)
    return cur.fetchall()

"""
Citation for the following code:
Date: 06/06/2024
Authors: Rami Albaroudi and Mohamed Saud, Group 13
Copied from https://github.com/osu-cs340-ecampus/flask-starter-app with minor modifications
"""

""" ___________ Listener for Website Hosting ___________ """
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 15999))
    app.run(port=port, debug=True)
