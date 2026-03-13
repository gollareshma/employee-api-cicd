from flask import Flask
from flask_mysqldb import MySQL
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

mysql = MySQL(app)

with app.app_context():
    cur = mysql.connection.cursor()

    try:
        cur.execute("ALTER TABLE employees ADD COLUMN role VARCHAR(100)")
    except:
        print("role column already exists")

    try:
        cur.execute("ALTER TABLE employees ADD COLUMN department_id INT")
    except:
        print("department_id column already exists")

    try:
        cur.execute("ALTER TABLE employees ADD COLUMN hire_date DATE")
    except:
        print("hire_date column already exists")

    try:
        cur.execute("ALTER TABLE employees ADD COLUMN status VARCHAR(20) DEFAULT 'active'")
    except:
        print("status column already exists")

    mysql.connection.commit()
    cur.close()

print("Employees table updated!")