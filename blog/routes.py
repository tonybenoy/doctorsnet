from datetime import datetime
from blog import app
import sqlite3
from werkzeug.security import generate_password_hash,check_password_hash
from werkzeug.urls import url_parse
from blog.forms import LoginForm,RegisterationForm,EditProfileForm, PostForm, CommentForm
from blog import login
from flask import render_template, flash, redirect,url_for,request
from flask_login import login_user,current_user,UserMixin,logout_user,login_required
import pdb

class User(UserMixin):
    pass


@login.user_loader
def load_user(id):
    user = User()
    user.id = id
    conn = sqlite3.connect('app.db')
    c = conn.cursor()
    c.execute("SELECT username FROM user WHERE id='%s'" %
              id)
    get = c.fetchone()
    conn.close()
    user.username = get[0]
    return user

@app.route('/user/<username>')
@login_required
def user(username):
    conn = sqlite3.connect('app.db')
    c = conn.cursor()
    c.execute("SELECT * FROM user WHERE username='%s'" %
              username)
    get = c.fetchone()
    user= User()
    user.username = get[1]
    user.id = get[2]
    c.execute("SELECT * FROM post WHERE user_id='%s'"%user.id )
    post = c.fetchall()
    posts = []
    for item in post:
        c.execute("SELECT username FROM user WHERE id='%s'" % item[3])
        username = c.fetchone()[0]
        a = {
            'author': {
                'username': username
            },
            'body': item[1],
            'time': item[2]
        }
        posts.append(a)
    conn.close()
    return render_template('user.html', user=user, posts=posts)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        conn = sqlite3.connect('app.db')
        c = conn.cursor()
        c.execute("UPDATE user SET last_seen = ? WHERE id= ?",
                  (datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"), current_user.id))
        conn.commit()
        conn.close()


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        body=form.post.data
        conn = sqlite3.connect('app.db')
        c = conn.cursor()
        print (current_user.username)
        c.execute("INSERT INTO post (body,timestamp,user_id,username) VALUES (?,?,?,?)",
                  (body, datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"), current_user.id,current_user.username))
        conn.commit()
        conn.close()
        flash('Your post is now live!')
        return redirect(url_for('index'))
    conn = sqlite3.connect('app.db')
    c = conn.cursor()
    c.execute("SELECT * from post ORDER BY timestamp DESC  LIMIT 25 ")
    post = c.fetchall()
    posts=[]
    for item in post:
        a={
            'author' :{
                'username': item[1]
            },
            'body' : item[2],
            'time' : item[3]
        }
        posts.append(a) 
    return render_template('index.html', title="Home", form=form, posts=posts)

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form= LoginForm()
    if form.validate_on_submit():
        conn =sqlite3.connect('app.db')
        c = conn.cursor()
        c.execute("SELECT id,hashedpass FROM user WHERE USERNAME='%s'"%form.username.data)
        passed = c.fetchone()
        conn.close()
        if passed == None:
            flash('Invalid username')
            return redirect(url_for('login'))
        else:
            if check_password_hash(passed[1], form.password.data) == False:
                flash('Invalid Password')
                return redirect(url_for('login'))
            else:
                user = User()
                user.id = passed[0]
                user.name = form.username.data
                login_user(user, remember = form.remember_me.data)
                next_page = request.args.get('next')
                if not next_page or url_parse(next_page).netloc != '':
                    next_page = url_for('index')
                return redirect(next_page)
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
        c.execute("SELECT * FROM user where username = ? OR email = ?",(username,email))
        usersreg = c.fetchmany()
        if usersreg == []:
            c.execute("INSERT INTO user (username,email,hashedpass) VALUES (?,?,?)",(username,email,hashedpass))
            conn.commit()
            conn.close() 
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('login'))
        else:
            flash('Email address or username already exist!')
        return redirect(url_for('register'))
    return render_template('register.html', title='Register', form=form)


@app.route('/post/<id>', methods=['GET', 'POST'])
@login_required
def post_page(id):
    form = CommentForm()
    if form.validate_on_submit():
        comment = form.comment.data
        conn = sqlite3.connect('app.db')
        c = conn.cursor()
        c.execute("INSERT INTO comment (post_id,body,timestamp,user_id,username) VALUES (?,?,?,?,?)",
                  (id,comment, datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"), current_user.id, current_user.username))
        conn.commit()
        conn.close()
        flash('Your comment is now posted!')
        return redirect(url_for('post_page',id=id))
    conn = sqlite3.connect('app.db')
    c = conn.cursor()
    c.execute("SELECT * FROM post WHERE id = ?",(id, ))
    post = c.fetchone()
    c.execute("SELECT * FROM comment WHERE post_id = ?",(id, ))
    comments = c.fetchall()
    comm=[]
    for item in comments:
        print(item)
        comm.append(
            {
                "comment": item[3],
                "username": item[2],
                "time":item[4]
            }
        )
    posts  = {
        "username" : post[1],
        "post" : post[2],
        "timestamp" : post[3],
        "comments" : comm
    }
    print (posts)
    return render_template('post.html', title='Post', form=form, posts=posts)



@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        conn = sqlite3.connect('app.db')
        c = conn.cursor()
        c.execute("UPDATE user SET username = ?, about = ? WHERE id= ?", (form.username.data,form.about_me.data,current_user.id))
        conn.commit()
        conn.close()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        conn = sqlite3.connect('app.db')
        c = conn.cursor()
        c.execute("SELECT USERNAME,about from user WHERE id= ?",( current_user.id))
        data=c.fetchone()
        conn.close()
        form.username.data = data[0]
        form.about_me.data = data[1]
    return render_template('edit_profile.html', title='Edit Profile',form=form)
