# KiloJulia 🥕

A database-driven nutrition and fitness tracking system designed for clinics managing multiple clients with robust reporting capabilities.

## Overview

KiloJulia addresses key challenges faced by nutrition clinics by providing:

- **Multi-client management** (100+ simultaneous clients)
- **Staff collaboration tools** with shared record access
- **Verified data entry** through clinician-controlled input
- **Comprehensive reporting** for informed decision-making
- **Scalable architecture** handling 200,000+ annual entries

## Key Features

### Client Management

- Track 5+ daily food/exercise entries per client
- Maintain historical progress records
- Manage client-staff assignments (500+ pairings)

### Staff Tools

- Multi-client dashboard views
- Instant access switching between clients
- Shared client assignments among staff

### Nutritional Database

- _n_ predefined food entries
- Standardized measurement tracking
- Exercise regimen documentation

## Database Structure

### Core Tables

1. **Clients** - Demographic and biometric data
2. **Staff** - Clinician credentials and assignments
3. **Foods** - Nutritional database with _n_ entries
4. **TrackedDays** - Daily client summaries
5. **ExerciseEntries** - Workout logging
6. **FoodEntries** - Meal tracking

### Scalability

- Designed for 100+ simultaneous clients
- Processes 200,000+ annual entries:
  - 180,000+ food/exercise records
  - 20,000+ food database entries
  - 500+ staff-client pairings

## Installation

### Clone repository

`git clone [repository_url]`

### Install dependencies

`pip install -r requirements.txt`

### Configure MySQL database

`mysql -u [username] -p < schema.sql`

### Prerequisites

- Python 3.8+
- MySQL 5.7+
- Modern web browser

## Known Issues

1. **Duplicate Operation Errors**  
   - Clicking buttons multiple times may display false errors  
   - Allow 2+ seconds between actions

2. **Rapid Action Conflicts**  
   - Quick successive clicks may trigger errors  
   - Complete one operation before initiating another

## Technologies Used

- **Frontend**: HTML5, CSS3, JavaScript
- **Backend**: Python/Flask
- **Database**: MySQL
- **APIs**: Fetch API for CRUD operations

## Citations
1. [Flask Starter App - OSU CS340](https://github.com/osu-cs340-ecampus/flask-starter-app)
2. [OSU CS340 Database Assignment Guidelines](https://canvas.oregonstate.edu/courses/1958399/assignments/9589656?module_item_id=24181840)
3. [Post Form Data Using JavaScript Fetch API](https://bobbyhadz.com/blog/post-form-data-using-javascript-fetch-api)
4. [Add onClick Event to Table Row in JavaScript](https://bobbyhadz.com/blog/add-onclick-event-to-table-row-in-javascript)
5. [Using the Fetch API - MDN Web Docs](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch)
6. [JavaScript Confirm Delete Before Delete Code](https://tutorial.eyehunts.com/js/javascript-confirm-delete-before-delete-code/)
7. [Carrot Emoji SVG - Twitter Twemoji](https://github.com/twitter/twemoji/blob/master/assets/svg/1f955.svg)

