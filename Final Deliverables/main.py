
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__, template_folder='./')

app.secret_key = 'password'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'job_recommender'

mysql = MySQL(app)

@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
		email = request.form['email']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE email = % s AND password = % s', (email, password, ))
		account = cursor.fetchone()
		if account:
			session['loggedin'] = True
			session['id'] = account['id']
			session['username'] = account['name']
			msg = 'Logged in successfully !'
			return render_template('index.html', msg = msg)
		else:
			msg = 'Incorrect username / password !'
	return render_template('login.html', msg = msg)

@app.route('/logout')
def logout():
	session.pop('loggedin', None)
	session.pop('id', None)
	session.pop('email', None)
	return redirect(url_for('login'))

@app.route('/register', methods =['GET', 'POST'])
def register():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'phone' in request.form :
		username = request.form['username']
		password = request.form['password']
		email = request.form['email']
		phone = request.form['phone']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE name = % s', (username, ))
		account = cursor.fetchone()
		if account:
			msg = 'Account already exists !'
		else:
			cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s, % s)', (email, password, username, phone))
			mysql.connection.commit()
			msg = 'You have successfully registered !'
	elif request.method == 'POST':
		msg = 'Please fill out the form !'
	return render_template('register.html', msg = msg)

@app.route('/check', methods =['GET', 'POST'])
def check():
	msg = ''
	if request.method == 'POST' and 'one' in request.form and 'two' in request.form and 'three' in request.form  and 'four' in request.form and 'five' in request.form and 'six' in request.form and 'sev' in request.form and 'eig' in request.form and 'nine' in request.form and 'ten' in request.form :
		one = int(request.form['one'])
		two = int(request.form['two'])
		three = int(request.form['three'])
		four = int(request.form['four'])
		five = int(request.form['five'])
		six = int(request.form['six'])
		sev = int(request.form['sev'])
		eig = int(request.form['eig'])
		nine = int(request.form['nine'])
		ten = int(request.form['ten'])
		sum = one+two+three+four+five+six+sev+eig+nine+ten
		if sum in range(0,14):
			msg='The best job for you might be Animal Care, Interior Designer, Event Planner, Athletic trainer, Fashion consultant, Chef'
		elif sum in range(15,19):
			msg='The best job for you might be Nurse, Therapist, Surgeon, Teacher, Lawyer, Economist, Real Estate Agent'
		elif sum in range(20,25):
			msg='The best job for you might be Blogger, Reporter, Social Media Influencer, Manager, Writer, Dietician'
		elif sum in range(26,50):
			msg='The best job for you might be Software Developer, Engineer, Fire Fighter, Musician, Actor'
		return render_template('result.html', msg = msg)
	elif request.method == 'POST':
		msg = 'login again'
		return render_template('login.html', msg = msg)

@app.route('/back', methods =['GET', 'POST'])
def back():
	msg=''
	return render_template('index.html', msg = msg)

if __name__ == '__main__':
    app.run(host='localhost', debug=True, threaded=False)