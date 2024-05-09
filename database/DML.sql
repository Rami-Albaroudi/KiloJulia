-- Citation for below queries:
-- Date: 09/05/2024
-- Authors: Rami Albaroudi, Mohamed Saud, Group 13
-- The queries below are fully original work

-- Query to get all staff members
SELECT * FROM Staff;

-- Query to add a new staff member
INSERT INTO Staff (staffName, staffEmail, staffCapacity, staffNote)
VALUES ($staffNameInput, $staffEmailInput, $staffCapacityInput, $staffNoteInput);

-- Query to update a staff member's details
UPDATE Staff
SET staffName = $staffNameInput, staffEmail = $staffEmailInput, 
    staffCapacity = $staffCapacityInput, staffNote = $staffNoteInput
WHERE staffID = $staffIDInput;

-- Query to delete a staff member
DELETE FROM Staff WHERE staffID = $staffIDInput;

-- Query to get all clients
SELECT * FROM Clients;

-- Query to add a new client
INSERT INTO Clients (clientName, clientEmail, clientSex, clientAge, clientHeight, 
                     clientWeight, clientActivityLevel, clientCalorieTarget, clientNote)
VALUES ($clientNameInput, $clientEmailInput, $clientSexInput, $clientAgeInput, 
        $clientHeightInput, $clientWeightInput, $clientActivityLevelInput, 
        $clientCalorieTargetInput, $clientNoteInput);

-- Query to update a client's details
UPDATE Clients
SET clientName = $clientNameInput, clientEmail = $clientEmailInput, 
    clientSex = $clientSexInput, clientAge = $clientAgeInput, 
    clientHeight = $clientHeightInput, clientWeight = $clientWeightInput,
    clientActivityLevel = $clientActivityLevelInput, 
    clientCalorieTarget = $clientCalorieTargetInput, clientNote = $clientNoteInput
WHERE clientID = $clientIDInput;

-- Query to delete a client
DELETE FROM Clients WHERE clientID = $clientIDInput;

-- Query to assign a client to a staff member
INSERT INTO StaffClients (staffID, clientID) 
VALUES ($staffIDInput, $clientIDInput);

-- Query to remove a client from a staff member
DELETE FROM StaffClients 
WHERE staffID = $staffIDInput AND clientID = $clientIDInput;

-- Query to get all tracked days for a client
SELECT * FROM TrackedDays WHERE clientID = $clientIDInput;

-- Query to add a new tracked day for a client
INSERT INTO TrackedDays (clientID, trackedDayDate, trackedDayTotalCalories, 
                         trackedDayCalorieTarget, trackedDayNote)
VALUES ($clientIDInput, $trackedDayDateInput, $trackedDayTotalCaloriesInput, 
        $trackedDayCalorieTargetInput, $trackedDayNoteInput);

-- Query to update a tracked day's details
UPDATE TrackedDays
SET trackedDayDate = $trackedDayDateInput, 
    trackedDayTotalCalories = $trackedDayTotalCaloriesInput,
    trackedDayCalorieTarget = $trackedDayCalorieTargetInput, 
    trackedDayNote = $trackedDayNoteInput
WHERE trackedDayID = $trackedDayIDInput AND clientID = $clientIDInput;

-- Query to delete a tracked day
DELETE FROM TrackedDays 
WHERE trackedDayID = $trackedDayIDInput AND clientID = $clientIDInput;

-- Query to get all foods
SELECT * FROM Foods;

-- Query to add a new food
INSERT INTO Foods (foodName, foodType, foodCaloriesPerGram, foodNote)
VALUES ($foodNameInput, $foodTypeInput, $foodCaloriesPerGramInput, $foodNoteInput);

-- Query to update a food's details
UPDATE Foods
SET foodName = $foodNameInput, foodType = $foodTypeInput, 
    foodCaloriesPerGram = $foodCaloriesPerGramInput, foodNote = $foodNoteInput
WHERE foodID = $foodIDInput;

-- Query to delete a food
DELETE FROM Foods WHERE foodID = $foodIDInput;

-- Query to get all food entries for a tracked day
SELECT * FROM FoodEntries 
WHERE trackedDayID = $trackedDayIDInput;

-- Query to add a new food entry for a tracked day
INSERT INTO FoodEntries (trackedDayID, foodID, foodEntryCalories, 
                         foodEntryGramWeight, foodEntryNote)
VALUES ($trackedDayIDInput, $foodIDInput, $foodEntryCaloriesInput, 
        $foodEntryGramWeightInput, $foodEntryNoteInput);

-- Query to update a food entry's details
UPDATE FoodEntries
SET foodID = $foodIDInput, foodEntryCalories = $foodEntryCaloriesInput, 
    foodEntryGramWeight = $foodEntryGramWeightInput, foodEntryNote = $foodEntryNoteInput
WHERE foodEntryID = $foodEntryIDInput AND trackedDayID = $trackedDayIDInput;

-- Query to delete a food entry
DELETE FROM FoodEntries
WHERE foodEntryID = $foodEntryIDInput AND trackedDayID = $trackedDayIDInput;

-- Query to get all exercise entries for a tracked day
SELECT * FROM ExerciseEntries
WHERE trackedDayID = $trackedDayIDInput;

-- Query to add a new exercise entry for a tracked day
INSERT INTO ExerciseEntries (trackedDayID, exerciseEntryName, exerciseEntryType, 
                             exerciseEntryCalories, exerciseEntryNote)
VALUES ($trackedDayIDInput, $exerciseEntryNameInput, $exerciseEntryTypeInput, 
        $exerciseEntryCaloriesInput, $exerciseEntryNoteInput);

-- Query to update an exercise entry's details
UPDATE ExerciseEntries
SET exerciseEntryName = $exerciseEntryNameInput, 
    exerciseEntryType = $exerciseEntryTypeInput,
    exerciseEntryCalories = $exerciseEntryCaloriesInput, 
    exerciseEntryNote = $exerciseEntryNoteInput
WHERE exerciseEntryID = $exerciseEntryIDInput AND trackedDayID = $trackedDayIDInput;

-- Query to delete an exercise entry
DELETE FROM ExerciseEntries
WHERE exerciseEntryID = $exerciseEntryIDInput AND trackedDayID = $trackedDayIDInput;
