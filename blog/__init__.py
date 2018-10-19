from flask import Flask
from config import Config
app = Flask(__name__)
app.config.from_object(Config)
from flask_login import LoginManager
login = LoginManager(app)
from pathlib import Path
app_db = Path('app.db')
if app_db.is_file() == False:
    import sqlite3
    conn =sqlite3.connect('app.db')
    c =conn.cursor()
    c.execute('''CREATE TABLE user (username text ,id integer ,about text ,hashedpass text, profile_pic blob)''')
    c.execute('''CREATE TABLE post (id integer, body text, timestamp text, user_id integer)''')
    conn.commit()
    conn.close()
from blog import routes
