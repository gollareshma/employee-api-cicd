from flask import Flask
from flask_mysqldb import MySQL
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

mysql = MySQL(app)

with app.app_context():
    cur = mysql.connection.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS departments (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        budget DECIMAL(15,2),
        location VARCHAR(100),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cur.execute("""
    INSERT INTO departments (name, budget, location) VALUES
    ('Engineering',2500000,'New York'),
    ('Marketing',1200000,'Los Angeles'),
    ('HR',800000,'Chicago'),
    ('Finance',1500000,'New York')
    """)

    mysql.connection.commit()
    cur.close()

print("Departments table created!")