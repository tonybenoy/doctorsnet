from blog import app
import sqlite3
from werkzeug.security import generate_password_hash,check_password_hash
from blog.forms import LoginForm,RegisterationForm
from blog import login
from flask import render_template, flash, redirect,url_for
from flask_login import login_user,current_user

conn = sqlite3.connect('example.db')
c = conn.cursor()

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
        c.execute("SELECT PASSWORD_HASH FROM USERS WHERE USERNAME='%s'"%form.username.data)
        print (c.fetchone())
        flash('Login requested for user {},remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html',title='Sign In', form=form)

@app.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return(url_for('index'))
    form = RegisterationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        hashedpass = generate_password_hash(form.password.data)
        conn = sqlite3.connect
