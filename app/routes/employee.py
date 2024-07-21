from flask import Blueprint, render_template, request, jsonify
from app import db
from app.models import Employee
from datetime import datetime

bp = Blueprint('employee', __name__)

@bp.route('/employees')
def employees():
    employees = Employee.query.all()
    return render_template('employee.html', employees=employees)

@bp.route('/employee/add', methods=['POST'])
def add_employee():
    name = request.form['name']
    position = request.form['position']
    phone = request.form['phone']
    hire_date = datetime.strptime(request.form['hire_date'], '%Y-%m-%d').date()

    new_employee = Employee(name=name, position=position, phone=phone, hire_date=hire_date)
    db.session.add(new_employee)
    db.session.commit()

    return jsonify({'success': True})

@bp.route('/employee/edit/<int:id>', methods=['POST'])
def edit_employee(id):
    employee = Employee.query.get_or_404(id)
    employee.name = request.form['name']
    employee.position = request.form['position']
    employee.phone = request.form['phone']
    employee.hire_date = datetime.strptime(request.form['hire_date'], '%Y-%m-%d').date()

    db.session.commit()

    return jsonify({'success': True})

@bp.route('/employee/delete/<int:id>', methods=['POST'])
def delete_employee(id):
    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()

    return jsonify({'success': True})

@bp.route('/employee/search')
def search_employee():
    query = request.args.get('query', '')
    employees = Employee.query.filter(
        (Employee.name.ilike(f'%{query}%')) |
        (Employee.position.ilike(f'%{query}%'))
    ).all()
    return jsonify([{
        'id': e.employee_id,
        'name': e.name,
        'position': e.position,
        'phone': e.phone,
        'hire_date': e.hire_date.strftime('%Y-%m-%d')
    } for e in employees])