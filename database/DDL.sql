/*
Citation for below code:
Date: 06/06/2024
Authors: OSU Staff
Copied from CS340 official course materials - Project Step 2 Draft page
URL: https://canvas.oregonstate.edu/courses/1958399/assignments/9589656?module_item_id=24181840
*/

-- Disable foreign key checks and autocommit to import the file
SET FOREIGN_KEY_CHECKS=0;
SET AUTOCOMMIT = 0;

/*
Citation for below code:
Date: 06/06/2024
Authors: Rami Albaroudi, Mohamed Saud, Group 13
Schema, Tables, Attributes, Keys, and Constraints were generated 
using MySQL Forward Engineering from our fully original MySQL Workbench schema and manually modified.
ON DELETE/UPDATE CASCADE statements were manually added to the CREATE TABLE statements. 
INSERT statements and sample data are fully original, manually created work. 
*/

/*_________ Create Statements for Database Tables _________*/

-- Create Table `Staff`
DROP TABLE IF EXISTS `Staff` ;
CREATE TABLE IF NOT EXISTS `Staff` (
  `staffID` INT NOT NULL AUTO_INCREMENT,
  `staffName` VARCHAR(255) NOT NULL,
  `staffEmail` VARCHAR(255) NOT NULL,
  `staffCapacity` ENUM('Available', 'Not Available') NOT NULL DEFAULT 'Available',
  `staffNote` VARCHAR(255) NULL DEFAULT NULL,
  PRIMARY KEY (`staffID`),
  UNIQUE INDEX `staffID_UNIQUE` (`staffID` ASC) VISIBLE,
  UNIQUE INDEX `staffEmail_UNIQUE` (`staffEmail` ASC) VISIBLE);

-- Create Table `Clients`
DROP TABLE IF EXISTS `Clients` ;
CREATE TABLE IF NOT EXISTS `Clients` (
  `clientID` INT NOT NULL AUTO_INCREMENT,
  `clientName` VARCHAR(255) NOT NULL,
  `clientEmail` VARCHAR(255) NOT NULL,
  `clientSex` ENUM('Male', 'Female') NOT NULL,
  `clientAge` INT UNSIGNED NOT NULL,
  `clientHeight` DECIMAL(5,1) UNSIGNED NOT NULL,
  `clientWeight` DECIMAL(5,1) UNSIGNED NOT NULL,
  `clientActivityLevel` ENUM('Sedentary', 'Light', 'Moderate', 'High', 'Athlete') NOT NULL,
  `clientCalorieTarget` INT UNSIGNED NOT NULL DEFAULT 0,
  `clientNote` VARCHAR(255) NULL DEFAULT NULL,
  PRIMARY KEY (`clientID`),
  UNIQUE INDEX `personID_UNIQUE` (`clientID` ASC) VISIBLE,
  UNIQUE INDEX `clientEmail_UNIQUE` (`clientEmail` ASC) VISIBLE);

-- Create Table `StaffClients`
DROP TABLE IF EXISTS `StaffClients` ;
CREATE TABLE IF NOT EXISTS `StaffClients` (
  `staffID` INT NOT NULL,
  `clientID` INT NOT NULL,
  PRIMARY KEY (`staffID`, `clientID`),
  INDEX `fk_Staff_has_Clients_Clients1_idx` (`clientID` ASC) VISIBLE,
  INDEX `fk_Staff_has_Clients_Staff1_idx` (`staffID` ASC) VISIBLE,
  CONSTRAINT `fk_Staff_has_Clients_Staff1`
    FOREIGN KEY (`staffID`)
    REFERENCES `Staff` (`staffID`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_Staff_has_Clients_Clients1`
    FOREIGN KEY (`clientID`)
    REFERENCES `Clients` (`clientID`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);

-- Create Table `TrackedDays`
DROP TABLE IF EXISTS `TrackedDays` ;
CREATE TABLE IF NOT EXISTS `TrackedDays` (
  `trackedDayID` INT NOT NULL AUTO_INCREMENT,
  `clientID` INT NOT NULL,
  `trackedDayDate` DATE NOT NULL DEFAULT CURRENT_DATE,
  `trackedDayCalorieTarget` INT NOT NULL DEFAULT 0,
  `trackedDayNote` VARCHAR(255) NULL DEFAULT NULL,
  PRIMARY KEY (`trackedDayID`),
  UNIQUE INDEX `dayID_UNIQUE` (`trackedDayID` ASC) VISIBLE,
  INDEX `fk_TrackedDays_Clients1_idx` (`clientID` ASC) VISIBLE,
  CONSTRAINT `fk_TrackedDays_Clients1`
    FOREIGN KEY (`clientID`)
    REFERENCES `Clients` (`clientID`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);

-- Create Table `Foods`
DROP TABLE IF EXISTS `Foods` ;
CREATE TABLE IF NOT EXISTS `Foods` (
  `foodID` INT NOT NULL AUTO_INCREMENT,
  `foodName` VARCHAR(255) NOT NULL,
  `foodType` ENUM('Fruits', 'Vegetables', 'Seafood', 'Dairy', 'Mushrooms', 'Grains', 'Meat', 
  'Spices', 'Nuts', 'Greens', 'Sweets', 'Oils and Sauces', 'Beverages', 'Alcohol', 'Soups', 
  'Baked Products', 'Fast Foods', 'Meals and Recipes', 'Other') NOT NULL,
  `foodCaloriesPerGram` DECIMAL(5,2) UNSIGNED NOT NULL,
  `foodNote` VARCHAR(255) NULL DEFAULT NULL,
  PRIMARY KEY (`foodID`),
  UNIQUE INDEX `uc_food_name` (`foodName` ASC) VISIBLE,
  UNIQUE INDEX `foodID_UNIQUE` (`foodID` ASC) VISIBLE);

-- Create Table `FoodEntries`
DROP TABLE IF EXISTS `FoodEntries` ;
CREATE TABLE IF NOT EXISTS `FoodEntries` (
  `foodEntryID` INT NOT NULL AUTO_INCREMENT,
  `trackedDayID` INT NOT NULL,
  `foodID` INT,
  `foodEntryCalories` INT UNSIGNED NOT NULL DEFAULT 0,
  `foodEntryGramWeight` INT UNSIGNED NOT NULL DEFAULT 0,
  `foodEntryNote` VARCHAR(255) NULL DEFAULT NULL,
  PRIMARY KEY (`foodEntryID`),
  INDEX `idx_entry_day` (`trackedDayID` ASC) VISIBLE,
  UNIQUE INDEX `entryID_UNIQUE` (`foodEntryID` ASC) VISIBLE,
  CONSTRAINT `fk_entry_day`
    FOREIGN KEY (`trackedDayID`)
    REFERENCES `TrackedDays` (`trackedDayID`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_entry_food`
    FOREIGN KEY (`foodID`)
    REFERENCES `Foods` (`foodID`)
    -- If food is deleted, keep the food entry, but set food ID to null. If food is updated, update the food entry. 
    ON DELETE SET NULL  
    ON UPDATE CASCADE);

-- Create Table `ExerciseEntries`
DROP TABLE IF EXISTS `ExerciseEntries` ;
CREATE TABLE IF NOT EXISTS `ExerciseEntries` (
  `exerciseEntryID` INT NOT NULL AUTO_INCREMENT,
  `trackedDayID` INT NOT NULL,
  `exerciseEntryName` VARCHAR(255) NOT NULL,
  `exerciseEntryType` ENUM('Cardio', 'Strength', 'Stretching', 'Balance', 'Other') NOT NULL,
  `exerciseEntryCalories` INT UNSIGNED NOT NULL DEFAULT 0,
  `exerciseEntryNote` VARCHAR(255) NULL DEFAULT NULL,
  PRIMARY KEY (`exerciseEntryID`),
  UNIQUE INDEX `exerciseID_UNIQUE` (`exerciseEntryID` ASC) VISIBLE,
  INDEX `fk_Exercises_Days1_idx` (`trackedDayID` ASC) VISIBLE,
  CONSTRAINT `fk_Exercises_Days1`
    FOREIGN KEY (`trackedDayID`)
    REFERENCES `TrackedDays` (`trackedDayID`)
    ON DELETE CASCADE
    ON UPDATE CASCADE);

/*_________ Insert Statements for Sample Data _________*/

-- Insert Staff
INSERT INTO Staff (staffID, staffName, staffEmail, staffCapacity, staffNote) VALUES
(1, 'John Adams', 'john.adams@nutriclinic.com', 'Not Available', 'Vegan Diets Specialist'),
(2, 'Charlene Yu', 'charlene.yu@nutriclinic.com', 'Not Available', 'On extended leave'),
(3, 'Susan Oyowe', 'susan.oyowe@nutriclinic.com', 'Available', 'Gluten Free Diets Specialist'),
(4, 'Mohrami Alsaud', 'mohrami.alsaud@nutriclinic.com', 'Available', NULL);

-- Insert Clients
INSERT INTO Clients (clientID, clientName, clientEmail, clientSex, clientAge, clientHeight, clientWeight, clientActivityLevel, clientCalorieTarget, clientNote) VALUES
(1, 'Muhammad Ali', 'muhammada@worldchamp.com', 'Male', 28, 189.2, 102.1, 'Athlete', 2900, 'Heart Condition'),
(2, 'Jessica Jackson', 'Jjackson@my.email.com', 'Female', 48, 168.5, 65.0, 'Moderate', 1700, 'Gluten Free'),
(3, 'Maria Filipe', 'matecka212@pmailer.org', 'Female', 25, 154.7, 58.2, 'Light', 1650, 'Vegan'),
(4, 'Akash Ashwal', 'akashhasw@mailme.com', 'Male', 38, 175.0, 92.0, 'High', 1850, NULL);

-- Insert StaffClients
INSERT INTO StaffClients (clientID, staffID)
VALUES
((SELECT clientID FROM Clients WHERE clientName = 'Muhammad Ali'), (SELECT staffID FROM Staff WHERE staffName = 'John Adams')),
((SELECT clientID FROM Clients WHERE clientName = 'Muhammad Ali'), (SELECT staffID FROM Staff WHERE staffName = 'Charlene Yu')),
((SELECT clientID FROM Clients WHERE clientName = 'Jessica Jackson'), (SELECT staffID FROM Staff WHERE staffName = 'John Adams')),
((SELECT clientID FROM Clients WHERE clientName = 'Maria Filipe'), (SELECT staffID FROM Staff WHERE staffName = 'Charlene Yu')),
((SELECT clientID FROM Clients WHERE clientName = 'Akash Ashwal'), (SELECT staffID FROM Staff WHERE staffName = 'Susan Oyowe')),
((SELECT clientID FROM Clients WHERE clientName = 'Akash Ashwal'), (SELECT staffID FROM Staff WHERE staffName = 'Mohrami Alsaud'));

-- Insert TrackedDays
INSERT INTO TrackedDays (trackedDayID, clientID, trackedDayDate, trackedDayCalorieTarget, trackedDayNote)
VALUES
(1, (SELECT clientID FROM Clients WHERE clientName = 'Muhammad Ali'), '2024-04-20', 2900, 'Client''s first day'),
(2, (SELECT clientID FROM Clients WHERE clientName = 'Jessica Jackson'), '2024-04-20', 1700, NULL),
(3, (SELECT clientID FROM Clients WHERE clientName = 'Muhammad Ali'), '2024-04-21', 2900, 'Bulking season'),
(4, (SELECT clientID FROM Clients WHERE clientName = 'Jessica Jackson'), '2024-04-21', 1700, 'Not Reported');

-- Insert Foods
INSERT INTO Foods (foodID, foodName, foodType, foodCaloriesPerGram, foodNote) VALUES
(1, 'Medium Banana', 'Fruits', 0.89, '5-7 in long'),
(2, 'Croissant, Medium, Store-Bought', 'Baked Products', 2.30, '6-8 in long'),
(3, 'Whole Milk', 'Dairy', 1.46, 'Approx. 3% Milkfat'),
(4, 'Cheeseburger, Restaurant, Fried', 'Fast Foods', 3.39, 'Average for restaurants');

-- Insert FoodEntries
INSERT INTO FoodEntries (foodEntryID, trackedDayID, foodID, foodEntryCalories, foodEntryGramWeight, foodEntryNote)
VALUES
(1, (SELECT trackedDayID FROM TrackedDays WHERE clientID = (SELECT clientID FROM Clients WHERE clientName = 'Muhammad Ali') AND trackedDayDate = '2024-04-20'), (SELECT foodID FROM Foods WHERE foodName = 'Medium Banana'), 89, 100, NULL),
(2, (SELECT trackedDayID FROM TrackedDays WHERE clientID = (SELECT clientID FROM Clients WHERE clientName = 'Muhammad Ali') AND trackedDayDate = '2024-04-20'), (SELECT foodID FROM Foods WHERE foodName = 'Croissant, Medium, Store-Bought'), 230, 100, NULL),
(3, (SELECT trackedDayID FROM TrackedDays WHERE clientID = (SELECT clientID FROM Clients WHERE clientName = 'Muhammad Ali') AND trackedDayDate = '2024-04-20'), (SELECT foodID FROM Foods WHERE foodName = 'Cheeseburger, Restaurant, Fried'), 1695, 500, 'Wendy''s Burger'),
(4, (SELECT trackedDayID FROM TrackedDays WHERE clientID = (SELECT clientID FROM Clients WHERE clientName = 'Jessica Jackson') AND trackedDayDate = '2024-04-20'), (SELECT foodID FROM Foods WHERE foodName = 'Croissant, Medium, Store-Bought'), 690, 300, 'Store-Bought'),
(5, (SELECT trackedDayID FROM TrackedDays WHERE clientID = (SELECT clientID FROM Clients WHERE clientName = 'Jessica Jackson') AND trackedDayDate = '2024-04-20'), (SELECT foodID FROM Foods WHERE foodName = 'Cheeseburger, Restaurant, Fried'), 1017, 300, 'Small Burger'),
(6, (SELECT trackedDayID FROM TrackedDays WHERE clientID = (SELECT clientID FROM Clients WHERE clientName = 'Muhammad Ali') AND trackedDayDate = '2024-04-21'), NULL, 250, 86, 'Calories from Chocolate Wrapper');

-- Insert ExerciseEntries
INSERT INTO ExerciseEntries (exerciseEntryID, trackedDayID, exerciseEntryName, exerciseEntryType, exerciseEntryCalories, exerciseEntryNote)
VALUES
(1, (SELECT trackedDayID FROM TrackedDays WHERE clientID = (SELECT clientID FROM Clients WHERE clientName = 'Muhammad Ali') AND trackedDayDate = '2024-04-20'), 'Light Jogging', 'Cardio', 250, NULL),
(2, (SELECT trackedDayID FROM TrackedDays WHERE clientID = (SELECT clientID FROM Clients WHERE clientName = 'Muhammad Ali') AND trackedDayDate = '2024-04-20'), 'Heavy Weightlifting', 'Strength', 400, 'Squats, Benchpress'),
(3, (SELECT trackedDayID FROM TrackedDays WHERE clientID = (SELECT clientID FROM Clients WHERE clientName = 'Jessica Jackson') AND trackedDayDate = '2024-04-20'), 'Rock Climbing', 'Other', 200, 'At a gym'),
(4, (SELECT trackedDayID FROM TrackedDays WHERE clientID = (SELECT clientID FROM Clients WHERE clientName = 'Jessica Jackson') AND trackedDayDate = '2024-04-20'), 'Light Yoga', 'Stretching', 100, NULL);

/*
Citation for below code:
Date: 06/06/2024
Authors: OSU Staff
Copied from CS340 official course materials - Project Step 2 Draft page
URL: https://canvas.oregonstate.edu/courses/1958399/assignments/9589656?module_item_id=24181840
*/

-- Re-enable foreign key checks and commit file
SET FOREIGN_KEY_CHECKS=1;
COMMIT;
