from blog import app
import sqlite3
from werkzeug.security import generate_password_hash,check_password_hash
from blog.forms import LoginForm,RegisterationForm
from blog import login
from flask import render_template, flash, redirect,url_for
from flask_login import login_user,current_user


def set_password(password):
    return generate_password_hash(password)
def check_password(hashedpassword,password):
    return check_password_hash(hashedpass,password)
    

@login.user_loader
def load_user(id):
    return int(id)

@app.route('/')
@app.route('/index')
def index():
    user = {'username':'Tony'}
    posts = [
            {
                'author' : {'username':'john'},
                'body' : 'Tony is the best'
            },
            {
                'author' : {'username':'tony'},
                'body' : 'Tony is da bomb'
            }
            ] 
    return render_template('index.html',title="Home",user=user,posts=posts)
@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form= LoginForm()
    if form.validate_on_submit():
        conn =sqlite3.connect('app.db')
        c = conn.cursor()
        c.execute("SELECT hashedpass FROM user WHERE USERNAME='%s'"%form.username.data)
        passed = c.fetchone()
        if passed == None:
            flash('Invalid username')
            return redirect(url_for('login'))
        else:
            if check_password_hash(passed[0], form.password.data) == False:
                flash('Invalid Password')
                return redirect(url_for('login'))
            else:
                login_user(user,remember=form.remember.data)
                return redirect(url_for('index'))
    return render_template('login.html',title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return(url_for('index'))
    form = RegisterationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        hashedpass = generate_password_hash(
            form.password.data, method='pbkdf2:sha256', salt_length=12)
        conn = sqlite3.connect('app.db')
        c = conn.cursor()
        c.execute("INSERT INTO user (username,email,hashedpass) VALUES (?,?,?)",(username,email,hashedpass))
        conn.commit()
        conn.close() 
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
