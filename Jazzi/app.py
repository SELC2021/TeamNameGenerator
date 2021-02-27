from flask import Flask, render_template, url_for, request, redirect
import mysql.connector
userDatabse = mysql.connector.connect(
    host='localhost',
    database='TeamNameGenerator',
    user='root',
    password='NewPassword'
)
app = Flask(__name__)

@app.route('/login') 
def login():
    return render_template('login.html')

@app.route('/register', methods =['GET', 'POST'])
def register():
    if request.method == 'POST':
    	firstname = request.form['firstname']
    	lastname = request.form['lastname']
    	email = request.form['email']
    	username = request.form['username']
    	password = request.form['password']
    	ccnumber = request.form['ccnumber']
    	expdate = request.form['expdate']
    	cvv = request.form['cvv']
    	zipcode = request.form['zipcode']

    	myCursor = userDatabse.cursor()

    	getNumberOfUsers = "SELECT * FROM NumberOfUsers"
    	myCursor.execute(getNumberOfUsers)
    	numUsers = myCursor.fetchall()
    	accountid = numUsers[0][0]

    	#myCursor = userDatabse.cursor()
    	insertUserDetails = "INSERT INTO Users (AccountID, FirstName, LastName, Email, Username, Password, CreditCardNumber, CreditCardExpDate, CreditCardCvv, ZipCode) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    	accountDetails = (accountid + 1, firstname, lastname, email, username, password, ccnumber, expdate, cvv, zipcode)
    	myCursor.execute(insertUserDetails, accountDetails)
    	
    	#myCursor3 = userDatabse.cursor()
    	updateNumberOfUsers = "UPDATE NumberOfUsers set number = number + 1"
    	myCursor.execute(updateNumberOfUsers)
    	myCursor.close()


    	userDatabse.commit()
    return render_template('registration2.html')

if __name__ == '__main__':
    app.run(debug=True)