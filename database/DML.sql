/* 
Citation for below code:
Date: 06/06/2024 
Authors: Rami Albaroudi, Mohamed Saud, Group 13
Original, hand-authored work 
*/

/*____________Queries for Staff____________*/

-- Query to get all staff members
SELECT * FROM Staff;

-- Query to add a new staff member using form inputs
INSERT INTO Staff (staffName, staffEmail, staffCapacity, staffNote)
VALUES ($staffNameInput, $staffEmailInput, $staffCapacityInput, $staffNoteInput);

-- Query to update a staff member's details using form inputs
UPDATE Staff 
SET 
staffName = $staffNameInput, 
staffEmail = $staffEmailInput, 
staffCapacity = $staffCapacityInput, 
staffNote = $staffNoteInput  
WHERE staffID = $staffIDInput;

-- Query to delete a staff member using form inputs
DELETE FROM Staff WHERE staffID = $staffIDInput;

/*____________ Queries for Clients ____________*/

-- Query to get all clients
SELECT * FROM Clients;

-- Query to add a new client using form inputs
INSERT INTO Clients (clientName, clientEmail, clientSex, clientAge, clientHeight, clientWeight, clientActivityLevel, clientCalorieTarget, clientNote)
VALUES ($clientNameInput, $clientEmailInput, $clientSexInput, $clientAgeInput, $clientHeightInput, $clientWeightInput, $clientActivityLevelInput,
$clientCalorieTargetInput, $clientNoteInput);

-- Query to update a client's details using form inputs
UPDATE Clients
SET 
clientName = $clientNameInput, 
clientEmail = $clientEmailInput,
clientSex = $clientSexInput, 
clientAge = $clientAgeInput,
clientHeight = $clientHeightInput, 
clientWeight = $clientWeightInput,
clientActivityLevel = $clientActivityLevelInput,
clientCalorieTarget = $clientCalorieTargetInput, 
clientNote = $clientNoteInput
WHERE clientID = $clientIDInput;

-- Query to delete a client using form inputs
DELETE FROM Clients WHERE clientID = $clientIDInput;

/*____________ Queries for Staff-Clients ____________*/
z
-- Query to get staff-clients assignments and staff/client names
SELECT sc.staffID, s.staffName, sc.clientID, c.clientName
FROM StaffClients sc 
JOIN Staff s ON sc.staffID = s.staffID
JOIN Clients c ON sc.clientID = c.clientID;

-- Query to create a staff-clients record using form inputs
INSERT INTO StaffClients (staffID, clientID)
VALUES ($staffIDInput, $clientIDInput);

-- Query to delete a staff-clients record using form inputs
DELETE FROM StaffClients
WHERE staffID = $staffIDInput AND clientID = $clientIDInput;

/*____________ Queries for Tracked Days ____________*/

-- Query to get all tracked days with calorie totals by client (All Food Entry Calories - All Exercise Entry calories) and client names
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
) 
AS trackedDayTotalCalories,
td.trackedDayCalorieTarget,
td.trackedDayNote,
c.clientName
FROM TrackedDays td
JOIN Clients c ON td.clientID = c.clientID;

-- Query to search tracked days by client name using form inputs
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
) 
AS trackedDayTotalCalories,
td.trackedDayCalorieTarget, 
td.trackedDayNote,
c.clientName  
FROM TrackedDays td
JOIN Clients c ON td.clientID = c.clientID
WHERE c.clientName LIKE %s;

-- Query to add a new tracked day for a client using form inputs
INSERT INTO TrackedDays (clientID, trackedDayDate, trackedDayTotalCalories, trackedDayCalorieTarget, trackedDayNote) 
VALUES ($clientIDInput, $trackedDayDateInput, $trackedDayTotalCaloriesInput, $trackedDayCalorieTargetInput, $trackedDayNoteInput);

-- Query to update a tracked day's details using form inputs
UPDATE TrackedDays  
SET 
trackedDayDate = $trackedDayDateInput,
trackedDayTotalCalories = $trackedDayTotalCaloriesInput, 
trackedDayCalorieTarget = $trackedDayCalorieTargetInput,
trackedDayNote = $trackedDayNoteInput
WHERE trackedDayID = $trackedDayIDInput AND clientID = $clientIDInput;

-- Query to delete a tracked day using form inputs
DELETE FROM TrackedDays
WHERE trackedDayID = $trackedDayIDInput AND clientID = $clientIDInput;

/*____________ Queries for Foods ____________*/

-- Query to get all foods
SELECT * FROM Foods;

-- Query to add a new food using form inputs
INSERT INTO Foods (foodName, foodType, foodCaloriesPerGram, foodNote) 
VALUES ($foodNameInput, $foodTypeInput, $foodCaloriesPerGramInput, $foodNoteInput);

-- Query to update a food's details using form inputs
UPDATE Foods
SET 
foodName = $foodNameInput, 
foodType = $foodTypeInput,  
foodCaloriesPerGram = $foodCaloriesPerGramInput, 
foodNote = $foodNoteInput
WHERE foodID = $foodIDInput;

-- Query to delete a food using form inputs
DELETE FROM Foods WHERE foodID = $foodIDInput;

/*____________ Queries for Food Entries ____________*/

-- Query to get all food entries with tracked day, client, and food details  
SELECT 
FoodEntries.foodEntryID, 
TrackedDays.trackedDayDate, 
Clients.clientName, 
Foods.foodName, 
FoodEntries.foodEntryCalories, 
FoodEntries.foodEntryGramWeight, 
FoodEntries.foodEntryNote
FROM FoodEntries
LEFT JOIN Foods ON FoodEntries.foodID = Foods.foodID
JOIN TrackedDays ON FoodEntries.trackedDayID = TrackedDays.trackedDayID
JOIN Clients ON TrackedDays.clientID = Clients.clientID;

-- Query to add a new food entry for a tracked day using form inputs
INSERT INTO FoodEntries (trackedDayID, foodID, foodEntryCalories, foodEntryGramWeight, foodEntryNote)
VALUES ($trackedDayIDInput, $foodIDInput, $foodEntryCaloriesInput, $foodEntryGramWeightInput, $foodEntryNoteInput);

-- Query to update a food entry's details using form inputs
UPDATE FoodEntries
SET 
foodID = $foodIDInput, 
foodEntryCalories = $foodEntryCaloriesInput,
foodEntryGramWeight = $foodEntryGramWeightInput, 
foodEntryNote = $foodEntryNoteInput  
WHERE foodEntryID = $foodEntryIDInput AND trackedDayID = $trackedDayIDInput;

-- Query to delete a food entry using form inputs
DELETE FROM FoodEntries  
WHERE foodEntryID = $foodEntryIDInput AND trackedDayID = $trackedDayIDInput;

-- Query to fetch client names for food entries
SELECT clientName FROM Clients;

-- Query to fetch food names for food entries
SELECT foodName FROM Foods;

-- Query to set food ID to NULL in a food entry using form inputs
UPDATE FoodEntries SET foodID = NULL WHERE foodEntryID = $foodEntryIDInput;

-- Query to fetch client names and tracked day dates for food entries
SELECT Clients.clientID, Clients.clientName, TrackedDays.trackedDayID, TrackedDays.trackedDayDate FROM Clients JOIN TrackedDays ON Clients.clientID = TrackedDays.clientID;

/*____________ Queries for Exercise Entries ____________*/

-- Query to get all exercise entries with tracked day and client names
SELECT  
ExerciseEntries.exerciseEntryID,
TrackedDays.trackedDayDate,
Clients.clientName,
ExerciseEntries.exerciseEntryName,
ExerciseEntries.exerciseEntryType,  
ExerciseEntries.exerciseEntryCalories,
ExerciseEntries.exerciseEntryNote
FROM ExerciseEntries  
JOIN TrackedDays ON ExerciseEntries.trackedDayID = TrackedDays.trackedDayID  
JOIN Clients ON TrackedDays.clientID = Clients.clientID;

-- Query to add a new exercise entry for a tracked day using form inputs
INSERT INTO ExerciseEntries (trackedDayID, exerciseEntryName, exerciseEntryType, exerciseEntryCalories, exerciseEntryNote) 
VALUES ($trackedDayIDInput, $exerciseEntryNameInput, $exerciseEntryTypeInput, $exerciseEntryCaloriesInput, $exerciseEntryNoteInput);

-- Query to update an exercise entry's details using form inputs
UPDATE ExerciseEntries
SET 
exerciseEntryName = $exerciseEntryNameInput,  
exerciseEntryType = $exerciseEntryTypeInput,
exerciseEntryCalories = $exerciseEntryCaloriesInput,
exerciseEntryNote = $exerciseEntryNoteInput  
WHERE exerciseEntryID = $exerciseEntryIDInput AND trackedDayID = $trackedDayIDInput;

-- Query to delete an exercise entry using form inputs
DELETE FROM ExerciseEntries  
WHERE exerciseEntryID = $exerciseEntryIDInput AND trackedDayID = $trackedDayIDInput;

-- Query to fetch client names and IDs for exercise entries
SELECT clientID, clientName FROM Clients;