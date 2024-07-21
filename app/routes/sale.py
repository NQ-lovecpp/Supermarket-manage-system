from flask import Blueprint, render_template, request, jsonify
from app import db
from app.models import Sale, Product, Employee
from datetime import datetime

bp = Blueprint('sale', __name__)

@bp.route('/sales')
def sales():
    sales = Sale.query.all()
    products = Product.query.all()
    employees = Employee.query.all()
    return render_template('sale.html', sales=sales, products=products, employees=employees)

@bp.route('/sale/add', methods=['POST'])
def add_sale():
    product_id = request.form['product_id']
    quantity = int(request.form['quantity'])
    unit_price = float(request.form['unit_price'])
    sale_date = datetime.strptime(request.form['sale_date'], '%Y-%m-%d').date()
    employee_id = request.form['employee_id']

    # 检查库存
    product = Product.query.get(product_id)
    if product.stock < quantity:
        return jsonify({'success': False, 'message': '库存不足'})

    new_sale = Sale(product_id=product_id, quantity=quantity, unit_price=unit_price, sale_date=sale_date, employee_id=employee_id)
    db.session.add(new_sale)

    # 更新库存
    product.stock -= quantity

    db.session.commit()

    return jsonify({'success': True})

@bp.route('/sale/search')
def search_sale():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    employee_id = request.args.get('employee_id')

    query = Sale.query

    if start_date:
        query = query.filter(Sale.sale_date >= datetime.strptime(start_date, '%Y-%m-%d').date())
    if end_date:
        query = query.filter(Sale.sale_date <= datetime.strptime(end_date, '%Y-%m-%d').date())
    if employee_id:
        query = query.filter(Sale.employee_id == employee_id)

    sales = query.all()
    return jsonify([{
        'id': s.sale_id,
        'product_name': s.product.name,
        'quantity': s.quantity,
        'unit_price': float(s.unit_price),
        'total_price': float(s.quantity * s.unit_price),
        'sale_date': s.sale_date.strftime('%Y-%m-%d'),
        'employee_name': s.employee.name
    } for s in sales])

@bp.route('/sale/statistics')
def sale_statistics():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    query = Sale.query

    if start_date:
        query = query.filter(Sale.sale_date >= datetime.strptime(start_date, '%Y-%m-%d').date())
    if end_date:
        query = query.filter(Sale.sale_date <= datetime.strptime(end_date, '%Y-%m-%d').date())

    sales = query.all()
    total_amount = sum(s.quantity * s.unit_price for s in sales)
    total_quantity = sum(s.quantity for s in sales)

    return jsonify({
        'total_amount': float(total_amount),
        'total_quantity': total_quantity
    })