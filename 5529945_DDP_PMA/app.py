import sqlite3
import os
from markupsafe import escape
import datetime
from flask import Flask, render_template, request, jsonify,url_for, redirect, abort, g,flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask("app")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a secure random key

# The database configuration
DATABASE = os.environ.get("FLASK_DATABASE", "app.db")

# Functions to help connect to the database
# And clean up when this application ends.
def get_db_connection():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

def init_db():
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            contact TEXT NOT NULL,
            reservation_time TEXT NOT NULL,
            num_people INTEGER NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html', restaurants=get_restaurants())

def get_restaurants():
    # 在这里你可以连接数据库或者提供一些餐厅的示例数据
    # 返回一个包含餐厅信息的列表，每个餐厅可以是一个字典
    return [
        {'name': 'Restaurant 1', 'description': 'Description 1'},
        {'name': 'Restaurant 2', 'description': 'Description 2'},
        {'name': 'Restaurant 3', 'description': 'Description 3'},
    ]

# @app.route('/category/<category_name>')
# def category(category_name):
#     # 在这里根据分类名获取相应的数据
#     # 然后将数据传递给模板，渲染页面
#     return render_template('index.html', category_name=category_name)

@app.route('/restaurant details')
def re_details():
    return render_template('R1.html')

# @app.route('/login')
# def login():
#     return render_template('login.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         user_id = request.form['user_id']
#         user = users.get(user_id)
#         if user:
#             # Assuming 'user' is an instance of User class
#             login_user(user)
#             return redirect(url_for('dashboard'))
#     return render_template('login.html')


# Check if the users table exists, if not, create it
# with app.app_context():
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS users (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             username TEXT NOT NULL,
#             password_hash TEXT NOT NULL
#         )
#     ''')
#     conn.commit()


# Registration route
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']

#         # Check if the username already exists
#         if username in users:
#             return jsonify({'success': False, 'message': 'Username already exists'})

#         # Hash the password before storing it
#         password_hash = generate_password_hash(password, method='sha256')

#         # Store the user in the database (you should use the database instead)
#         user_id = len(users) + 1
#         users[username] = {'id': user_id, 'username': username, 'password_hash': password_hash}

#         return jsonify({'success': True, 'message': 'Registration successful'})

#     return render_template('register.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()

        # 检查用户名是否已经存在
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cursor.fetchone()

        if user:
            conn.close()
            return render_template('register.html', message='Username already exists')

        # 将用户名和加密后的密码插入数据库
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        conn.close()

        flash('Registration successful. Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', message='')

# Login route
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']

#         # Check if the username exists
#         if username not in users:
#             return jsonify({'success': False, 'message': 'Username does not exist'})

#         # Check if the password is correct
#         user = users[username]
#         if not check_password_hash(user['password_hash'], password):
#             return jsonify({'success': False, 'message': 'Incorrect password'})

#         # Log in the user (you should use Flask-Login for a complete login system)
#         # For simplicity, this example just redirects to the home page
#         return redirect(url_for('index'))

#     return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()

        # 检查用户名是否存在
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cursor.fetchone()
        conn.close()

        # 验证密码
        if user and check_password_hash(user[2], password):
            # return f'登录成功，欢迎 {username}！'
            flash('Login successful!', 'success')
            # 可以在这里设置用户 session
            return redirect(url_for('index'))
        else:
            flash('Login failed. Check your username and password.', 'danger')
            # return render_template('login.html', message='用户名或密码错误')

    return render_template('login.html', message='')

@app.route('/reserve')
def reserve():
    return render_template('reserve.html')

@app.route('/submit_reserve', methods=['POST'])
def submit_reserve():
    if request.method == 'POST':
        # Get booking information from the form
        name = request.form.get('name')
        contact = request.form.get('contact')
        reservation_time = request.form.get('reservation_time')
        num_people = int(request.form.get('num_people'))

        # Simple input validation to ensure necessary information is provided
        if not name or not contact or not reservation_time or num_people <= 0:
            return "Please provide complete and valid booking information"

        # Store booking information in the database
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()
        
    try:

        cursor.execute('''
            INSERT INTO bookings (name, contact, reservation_time, num_people)
            VALUES (?, ?, ?, ?)
        ''', (name, contact, reservation_time, num_people))

        conn.commit()
        print("Booking data inserted successfully")
    except Exception as e:
        print(f"Error inserting data: {e}")
        conn.rollback()
    finally:
        conn.close()

        # Provide feedback for successful booking
        # return f"Booking successful! Thank you, {name}!"
        return render_template('reserve.html', message='Booking successful! Thank you')


if __name__ == '__main__':
    app.run(debug=True)