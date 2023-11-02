from flask import Flask, render_template
import mysql.connector
import os

app = Flask(__name__)

# MySQL database connection configuration
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='TgFRYUJ@03',
    database='project'
)

# Create a cursor for executing SQL queries
cursor = db.cursor()

@app.route('/')
def home():
    # Execute an SQL query to fetch data from the database
    cursor.execute("SELECT * FROM follows")
    data = cursor.fetchall()
    return render_template('home.html', data=data)

@app.route('/print_working_directory')
def print_working_directory():
    return os.getcwd()

if __name__ == "__main__":
    app.run(debug=True)
