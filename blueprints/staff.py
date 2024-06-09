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