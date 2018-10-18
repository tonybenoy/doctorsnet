from blog import app
from blog.forms import LoginForm
from flask import render_template
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
@app.route('/login')
def login():
    form= LoginForm()
    return render_template('login.html',title='Sign In', form=form)
