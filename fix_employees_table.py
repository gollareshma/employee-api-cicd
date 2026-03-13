from flask import Flask
from flask_mysqldb import MySQL
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

mysql = MySQL(app)

with app.app_context():
    cur = mysql.connection.cursor()

    cur.execute("""
    ALTER TABLE employees
    ADD COLUMN phone VARCHAR(20)
    """)

    mysql.connection.commit()
    cur.close()

print("Phone column added to employees table!")