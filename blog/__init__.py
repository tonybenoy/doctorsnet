from flask import Flask
from config import Config
from flask_bootstrap import Bootstrap
import sqlite3
app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config.from_object(Config)
from flask_login import LoginManager
login = LoginManager(app)
login.login_view = 'login'
from pathlib import Path
app_db = Path('app.db')
if app_db.is_file() == False:
    conn = sqlite3.connect('app.db')                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
    c =conn.cursor()
    c.execute('''CREATE TABLE user (last_seen text, username text UNIQUE NOT NULL,id integer PRIMARY KEY AUTOINCREMENT,about text ,hashedpass text,email text ,profile_pic blob)''')
    c.execute('''CREATE TABLE post (id integer PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,username text, body text, timestamp text, user_id integer)''')
    c.execute('''CREATE TABLE comment (id integer PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,user_id id,username text, body text, timestamp text, post_id integer)''')
    conn.commit()
    conn.close()
from blog import routes
