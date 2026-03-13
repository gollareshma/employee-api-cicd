from flask import Blueprint, jsonify
from app.auth import token_required

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/headcount', methods=['GET'])
@token_required
def headcount():
    """Employees count by department"""
    mysql = analytics_bp.mysql
    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT 
            d.name AS department,
            COUNT(e.id) AS total_employees,
            ROUND(AVG(e.salary),2) AS avg_salary
        FROM departments d
        LEFT JOIN employees e ON d.id = e.department_id
        GROUP BY d.name
        ORDER BY total_employees DESC
    """)

    data = cur.fetchall()
    cur.close()

    return jsonify(data), 200


@analytics_bp.route('/salary-bands', methods=['GET'])
@token_required
def salary_bands():
    """Salary distribution"""
    mysql = analytics_bp.mysql
    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT
            CASE
                WHEN salary < 70000 THEN 'Under 70K'
                WHEN salary BETWEEN 70000 AND 100000 THEN '70K-100K'
                WHEN salary BETWEEN 100001 AND 130000 THEN '100K-130K'
                ELSE 'Above 130K'
            END AS salary_band,
            COUNT(*) AS employees
        FROM employees
        GROUP BY salary_band
    """)

    data = cur.fetchall()
    cur.close()

    return jsonify(data), 200