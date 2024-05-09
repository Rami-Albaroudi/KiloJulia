# KiloJulia

Most nutrition apps only track data for a single client at a time. In contrast, NutriClinic, a nutrition and fitness clinic, needs to track data for up to 100 unique clients at a time. NutriClinic provides all clients with food scales, fitness watches, and a log sheet that clients fill out daily to submit logs to NutriClinic at the end of every week. NutriClinic used to ask clients to input data directly into an app and export the reports, but its staff have found that clients record and enter data inaccurately, and they would prefer to verify client logs as they enter it into a database themselves. In addition, NutriClinic staff members often have multiple clients at a time, and need easy access to client records so they can swap clients if they are unavailable. Using KiloJulia’s database-driven website, NutriClinic staff can conveniently enter all their clients’ exercise and food logs using pre-defined databases of foods to create accurate records. The database can be used to produce various reports that help staff make informed decisions about their clients’ diet and exercise, track progress over time, and help clients achieve health and fitness goals. KiloJulia also allows multiple clients to be assigned to multiple staff members and vice versa, providing convenient record sharing to make sure assigned staff members always understand their clients’ situation. KiloJulia is designed to store and process nutritional data for up to 100 clients, each associated with multiple staff members as well as multiple meals and exercises per day. Overall, every instance of KiloJulia is designed to handle up to 200,000 data entries per year (100 clients * 365 days * 5 food and exercise entries = 182,500 entries + 17,000 foods + 500 staff and client pairings). The KiloJulia database consists of 6 primary tables representing each category of data that NutriClinic needs to track.   
 
1.	Clients
2.	Staff
3.	Foods 
4.	TrackedDays
5.	ExerciseEntries
6.	FoodEntries
