from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import MySQLdb.cursors
from datetime import datetime
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# ----------------- MySQL Configuration -----------------

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'mypackingbuddy'
app.config['MYSQL_DB'] = 'my_packing_buddy'

mysql = MySQL(app)

# ----------------- Weather API -----------------


API_KEY = 'YOUR_OPENWEATHERMAP_API_KEY'

def get_weather(city):
    try:
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
        response = requests.get(url)
        data = response.json()
        if data.get('cod') != 200:
            return None
        return {
            'city': data['name'],
            'country': data['sys']['country'],
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description'],
            'icon': f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png"
        }
    except:
        return None

# ----------------- Signup -----------------

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        phone = request.form.get('phone')
        gender = request.form.get('gender')
        age = request.form.get('age')

        if not username or not email or not password or not phone or not gender or not age:
            flash("Please fill all fields", "danger")
            return redirect(url_for('signup'))

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM user WHERE username=%s", (username,))
        account = cursor.fetchone()
        if account:
            flash("Username already exists!", "warning")
            cursor.close()
            return redirect(url_for('signup'))

        hashed_password = generate_password_hash(password)
        cursor.execute("""
            INSERT INTO user (username, email, phone, age, password, gender, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (username, email, phone, age, hashed_password, gender, datetime.now()))
        mysql.connection.commit()
        cursor.close()

        flash("Account created successfully! Please login.", "success")
        return redirect(url_for('login'))

    return render_template('signup.html')

# ----------------- Login -----------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username_or_email = request.form['username']  # user can enter username or email
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM user WHERE username=%s OR email=%s", 
                       (username_or_email, username_or_email))
        account = cursor.fetchone()

        if account and check_password_hash(account['password'], password):
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Incorrect username/email or password!', 'danger')
    return render_template('login.html')

# ----------------- Logout -----------------

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))

# ----------------- Dashboard -----------------

@app.route('/')
@app.route('/dashboard')
def dashboard():
    if 'loggedin' in session:
        return render_template('dashboard.html', username=session['username'])
    return redirect(url_for('login'))

# ----------------- Destination -----------------

@app.route('/destination', methods=['GET', 'POST'])
def destination():
    city = None
    weather = None
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        city = request.form.get('city')
        weather = get_weather(city)
        if not weather:
            flash("City not found or API error", "danger")
    return render_template('destination.html', city=city, weather=weather)

# ----------------- Gender selection pages -----------------

@app.route('/beachgender')
def beach_gender():
    return render_template('beach/beachgender.html')

@app.route('/mountaingender')
def mountain_gender():
    return render_template('mountain/mountaingender.html')

@app.route('/snowvalleygender')
def snowvalley_gender():
    return render_template('snowvalley/snowvalleygender.html')

@app.route('/forestgender')
def forest_gender():
    return render_template('forest/forestgender.html')

@app.route('/lakegender')
def lake_gender():
    return render_template('lake/lakegender.html')

@app.route('/desertgender')
def desert_gender():
    return render_template('desert/desertgender.html')

# ----------------- Male, Female, Baby pages -----------------
# Beach

@app.route('/malebeach')
def male_beach():
    return render_template('beach/malebeach.html')

@app.route('/femalebeach')
def female_beach():
    return render_template('beach/femalebeach.html')

@app.route('/babybeach')
def baby_beach():
    return render_template('beach/babybeach.html')

# Mountain

@app.route('/malemountain')
def male_mountain():
    return render_template('mountain/malemountain.html')

@app.route('/femalemountain')
def female_mountain():
    return render_template('mountain/femalemountain.html')

@app.route('/babymountain')
def baby_mountain():
    return render_template('mountain/babymountain.html')

# Snow Valley

@app.route('/malesnowvalley')
def male_snowvalley():
    return render_template('snowvalley/malesnowvalley.html')

@app.route('/femalesnowvalley')
def female_snowvalley():
    return render_template('snowvalley/femalesnowvalley.html')

@app.route('/babysnowvalley')
def baby_snowvalley():
    return render_template('snowvalley/babysnowvalley.html')

# Forest

@app.route('/maleforest')
def male_forest():
    return render_template('forest/maleforest.html')

@app.route('/femaleforest')
def female_forest():
    return render_template('forest/femaleforest.html')

@app.route('/babyforest')
def baby_forest():
    return render_template('forest/babyforest.html')

# Lake

@app.route('/malelake')
def male_lake():
    return render_template('lake/malelake.html')

@app.route('/femalelake')
def female_lake():
    return render_template('lake/femalelake.html')

@app.route('/babylake')
def baby_lake():
    return render_template('lake/babylake.html')

# Desert

@app.route('/maledesert')
def male_desert():
    return render_template('desert/maledesert.html')

@app.route('/femaledesert')
def female_desert():
    return render_template('desert/femaledesert.html')

@app.route('/babydesert')
def baby_desert():
    return render_template('desert/babydesert.html')

# ----------------- Run App -----------------

if __name__ == '__main__':
    app.run(debug=True, port=5002)







