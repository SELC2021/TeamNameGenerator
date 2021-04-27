from flask import Flask, render_template, url_for, request, redirect
import mysql.connector


userDatabse = mysql.connector.connect(
    host='localhost',
    database='TeamNameGenerator',
    user='root',
    password='NewPassword'
)
app = Flask(__name__)

@app.route('/logout', methods =['GET', 'POST'])
def logout():
    if request.method == "POST":
        login()
    return render_template('login.html')

@app.route('/create', methods =['GET', 'POST']) 
def create():
    if request.method == "POST":
        return redirect('/profile')
    return render_template('create.html')

@app.route('/shop', methods =['GET', 'POST']) 
def shop():
    if request.method == 'POST':
        try:
            accountID = loggedInAccountId
            numCredits = request.form['tokens']
            tokenCursor = userDatabse.cursor()
            updateNumberOfTokens = f"UPDATE Users set Credits = Credits + '{numCredits}' WHERE AccountId = '{accountID}'"
            tokenCursor.execute(updateNumberOfTokens)
            tokenCursor.close()
            userDatabse.commit()
            if (numCredits > 0):
                return redirect('/profile')
        except:
            return redirect('/login')
    return render_template('shop.html')  

@app.route('/profile')
def profile():
    try:
        accountID = loggedInAccountId

        userInfoCursor = userDatabse.cursor()
        getFirstName = f"SELECT FirstName FROM Users WHERE AccountID = '{accountID}'"
        userInfoCursor.execute(getFirstName)
        FirstName = userInfoCursor.fetchall()
        
        getLastName = f"SELECT LastName FROM Users WHERE AccountID = '{accountID}'"
        userInfoCursor.execute(getLastName)
        LastName = userInfoCursor.fetchall()

        getUsername = f"SELECT Username FROM Users WHERE AccountID = '{accountID}'"
        userInfoCursor.execute(getUsername)
        Username = userInfoCursor.fetchall()

        getNumCredits = f"SELECT Credits FROM Users WHERE AccountID = '{accountID}'"
        userInfoCursor.execute(getNumCredits)
        Credits = userInfoCursor.fetchall()
        print(Credits)
        userInfoCursor.close()
        userDatabse.commit()
    except:
        return redirect('/login')
    return render_template('profile.html', firstName = FirstName[0][0], lastName = LastName[0][0], numCredits = Credits[0][0], userName = Username[0][0])


@app.route('/browse')
def browse():
    try:
        accountID = loggedInAccountId

        userInfoCursor = userDatabse.cursor()
        getFirstName = f"SELECT FirstName FROM Users WHERE AccountID = '{accountID}'"
        userInfoCursor.execute(getFirstName)
        FirstName = userInfoCursor.fetchall()
        
        getLastName = f"SELECT LastName FROM Users WHERE AccountID = '{accountID}'"
        userInfoCursor.execute(getLastName)
        LastName = userInfoCursor.fetchall()

        getNumCredits = f"SELECT Credits FROM Users WHERE AccountID = '{accountID}'"
        userInfoCursor.execute(getNumCredits)
        Credits = userInfoCursor.fetchall()
        print(Credits)
        userInfoCursor.close()
        userDatabse.commit()
    except:
        return redirect('/login')
    return render_template('browse.html', firstName = FirstName[0][0], lastName = LastName[0][0], numCredits = Credits[0][0])

@app.route('/login', methods =['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['login_username']
        password = request.form['login_password']
        loginCursor = userDatabse.cursor()
        checkAccount = f"SELECT AccountID, Username, Password FROM Users WHERE Username = '{username}'"
        loginCursor.execute(checkAccount)
        accountInfo = loginCursor.fetchall()
        loginCursor.close()
        userDatabse.commit()
        try: 
            if username in accountInfo[0]:
                if password in accountInfo[0]:
                    print("Logged in successfully!") 
                    global loggedInAccountId
                    loggedInAccountId = accountInfo[0][0]
                    return redirect('/browse')
                else:
                    print("Wrong password!")
        except:
            print("Account not found!")
    return render_template('login.html')  


@app.route('/register', methods =['GET', 'POST'])
def register():
    if request.method == 'POST' and request.form['password'] == request.form['confirm_password']:
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
    	insertUserDetails = "INSERT INTO Users (AccountID, FirstName, LastName, Email, Username, Password, CreditCardNumber, CreditCardExpDate, CreditCardCvv, ZipCode, Credits) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    	accountDetails = (accountid + 1, firstname, lastname, email, username, password, ccnumber, expdate, cvv, zipcode, 0)
    	myCursor.execute(insertUserDetails, accountDetails)
    	
    	#myCursor3 = userDatabse.cursor()
    	updateNumberOfUsers = "UPDATE NumberOfUsers set number = number + 1"
    	myCursor.execute(updateNumberOfUsers)
    	myCursor.close()
    	userDatabse.commit()
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)