from flask import Blueprint, request, jsonify
from app.auth import token_required, admin_required

employees_bp = Blueprint('employees', __name__)

@employees_bp.route('/', methods=['GET'])
@token_required
def get_all_employees():
    """Get all employees"""
    mysql = employees_bp.mysql
    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT e.id, e.name, e.email, e.phone, e.role,
               e.salary, e.hire_date, e.status,
               d.name as department
        FROM employees e
        LEFT JOIN departments d ON e.department_id = d.id
        ORDER BY e.created_at DESC
    """)

    employees = cur.fetchall()
    cur.close()

    return jsonify(employees), 200


@employees_bp.route('/<int:id>', methods=['GET'])
@token_required
def get_employee(id):
    """Get single employee"""
    mysql = employees_bp.mysql
    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT e.*, d.name as department
        FROM employees e
        LEFT JOIN departments d ON e.department_id = d.id
        WHERE e.id = %s
    """, (id,))

    employee = cur.fetchone()
    cur.close()

    if not employee:
        return jsonify({"error": "Employee not found"}), 404

    return jsonify(employee), 200


@employees_bp.route('/', methods=['POST'])
@admin_required
def create_employee():
    """Create employee (admin only)"""
    data = request.get_json()

    mysql = employees_bp.mysql
    cur = mysql.connection.cursor()

    cur.execute("""
        INSERT INTO employees
        (name, email, phone, role, department_id, salary, hire_date)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """, (
        data['name'],
        data['email'],
        data.get('phone'),
        data['role'],
        data['department_id'],
        data['salary'],
        data['hire_date']
    ))

    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "Employee created"}), 201


@employees_bp.route('/<int:id>', methods=['PUT'])
@admin_required
def update_employee(id):
    """Update employee"""
    data = request.get_json()

    mysql = employees_bp.mysql
    cur = mysql.connection.cursor()

    cur.execute("""
        UPDATE employees
        SET name=%s,email=%s,phone=%s,role=%s,salary=%s,status=%s
        WHERE id=%s
    """, (
        data['name'],
        data['email'],
        data.get('phone'),
        data['role'],
        data['salary'],
        data['status'],
        id
    ))

    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "Employee updated"}), 200


@employees_bp.route('/<int:id>', methods=['DELETE'])
@admin_required
def delete_employee(id):
    """Delete employee"""
    mysql = employees_bp.mysql
    cur = mysql.connection.cursor()

    cur.execute("DELETE FROM employees WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "Employee deleted"}), 200