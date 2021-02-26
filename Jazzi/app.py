from flask import Flask, render_template, url_for, request, redirect
import mysql.connector
userDatabse = mysql.connector.connect(
    host='localhost',
    database='TeamNameGenerator',
    user='root',
    password='Chimaobim3'
)
app = Flask(__name__)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register', methods =['GET', 'POST'])
def register():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
    	username = request.form['username']
    	password = request.form['password']
    	email = request.form['email']
    	
    	myCursor = userDatabse.cursor()

    	getNumberOfUsers = "SELECT * FROM NumberOfUsers"
    	myCursor.execute(getNumberOfUsers)
    	numUsers = myCursor.fetchall()
    	accountid = numUsers[0][0]

    	#myCursor = userDatabse.cursor()
    	insertUserDetails = "INSERT INTO Users (AccountID, Username, Password, Email) VALUES (%s, %s, %s, %s)"
    	accountDetails = (accountid + 1, username, password, email)
    	myCursor.execute(insertUserDetails, accountDetails)
    	
    	#myCursor3 = userDatabse.cursor()
    	updateNumberOfUsers = "UPDATE NumberOfUsers set number = number + 1"
    	myCursor.execute(updateNumberOfUsers)
    	myCursor.close()


    	userDatabse.commit()
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)