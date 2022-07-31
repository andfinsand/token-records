from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_bcrypt import Bcrypt
from flask_app.models.user import User

bcrypt = Bcrypt(app)

# Index and Login

@app.route('/')
def index():
    return render_template('login_register/index.html')

# Register

@app.route('/register')
def register():
    return render_template('login_register/register.html')

# Register process form

@app.route('/process_registration', methods=['POST'])
def process_register():
    if not User.validate_new_user(request.form):
        return redirect('/register')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        "email": request.form['email'],
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "password": pw_hash
    }
    user_id = User.create(data)
    session['user_id'] = user_id
    return redirect('/')

# Login process form

@app.route('/process_login' , methods = ['POST'])
def process_login():
    data = {'email' : request.form['email']}
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash('Invalid Email/Password' , 'login')
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash('Invalid Email/Password' , 'login')
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect('/collection')

# Logout

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')