SideQuest
SideQuest is a web application where users can create and browse sidequests, which area small tasks or activities to do when bored.
Features

Users can create an account and log in/out, or browse without an account
Logged-in users can create, edit and delete sidequests
Logged-in users can mark a sidequest as completed or incomplete (per user)
Sidequests can be tagged with one or more categories
Sidequests can be searched by keyword, difficulty, duration and tag
Each sidequest page shows comments from other users
User pages show statistics and a list of quests added by that user

Setup

Install Flask: pip install flask

Create config.py in the project root with: secret_key = "your_secret_key_here"

Generate a secure key with: python -c "import secrets; print(secrets.token_hex(32))"


Create the database: sqlite3 database.db < schema.sql

Run the application: flask run
if flask isn't in path, try:python -m flask run

Open in browser: http://127.0.0.1:5000

Testing

Register an account on the register page
Log in
Create a new sidequest using the "New quest" link
Open a quest to edit, delete, complete or comment on it
Try searching and filtering on the search page
Check the user page by clicking a username
