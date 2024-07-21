from flask import Blueprint, render_template, request, jsonify
from app import db
from app.models import Sale, Product, Employee
from sqlalchemy import func
from datetime import datetime, timedelta

bp = Blueprint('analysis', __name__)

@bp.route('/analysis')
def analysis():
    return render_template('analysis.html')

@bp.route('/analysis/sales_trend')
def sales_trend():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    interval = request.args.get('interval', 'day')

    query = db.session.query(
        func.date_trunc(interval, Sale.sale_date).label('date'),
        func.sum(Sale.quantity * Sale.unit_price).label('total_sales')
    )

    if start_date:
        query = query.filter(Sale.sale_date >= datetime.strptime(start_date, '%Y-%m-%d'))
    if end_date:
        query = query.filter(Sale.sale_date <= datetime.strptime(end_date, '%Y-%m-%d'))

    result = query.group_by(func.date_trunc(interval, Sale.sale_date)).order_by('date').all()

    return jsonify([{
        'date': item.date.strftime('%Y-%m-%d'),
        'total_sales': float(item.total_sales)
    } for item in result])

@bp.route('/analysis/top_products')
def top_products():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    query = db.session.query(
        Product.name,
        func.sum(Sale.quantity).label('total_quantity'),
        func.sum(Sale.quantity * Sale.unit_price).label('total_sales')
    ).join(Sale)

    if start_date:
        query = query.filter(Sale.sale_date >= datetime.strptime(start_date, '%Y-%m-%d'))
    if end_date:
        query = query.filter(Sale.sale_date <= datetime.strptime(end_date, '%Y-%m-%d'))

    result = query.group_by(Product.name).order_by(func.sum(Sale.quantity * Sale.unit_price).desc()).limit(10).all()

    return jsonify([{
        'product_name': item.name,
        'total_quantity': item.total_quantity,
        'total_sales': float(item.total_sales)
    } for item in result])

@bp.route('/analysis/employee_performance')
def employee_performance():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    query = db.session.query(
        Employee.name,
        func.sum(Sale.quantity).label('total_quantity'),
        func.sum(Sale.quantity * Sale.unit_price).label('total_sales')
    ).join(Sale)

    if start_date:
        query = query.filter(Sale.sale_date >= datetime.strptime(start_date, '%Y-%m-%d'))
    if end_date:
        query = query.filter(Sale.sale_date <= datetime.strptime(end_date, '%Y-%m-%d'))

    result = query.group_by(Employee.name).order_by(func.sum(Sale.quantity * Sale.unit_price).desc()).all()

    return jsonify([{
        'employee_name': item.name,
        'total_quantity': item.total_quantity,
        'total_sales': float(item.total_sales)
    } for item in result])

@bp.route('/analysis/inventory_turnover')
def inventory_turnover():
    products = Product.query.all()
    current_date = datetime.now()
    start_date = current_date - timedelta(days=30)  # 计算最近30天的周转率

    result = []
    for product in products:
        sales = db.session.query(func.sum(Sale.quantity)).filter(
            Sale.product_id == product.product_id,
            Sale.sale_date >= start_date,
            Sale.sale_date <= current_date
        ).scalar() or 0

        turnover_rate = sales / (product.stock or 1)  # 避免除以零

        result.append({
            'product_name': product.name,
            'current_stock': product.stock,
            'sales_last_30_days': sales,
            'turnover_rate': round(turnover_rate, 2)
        })

    return jsonify(sorted(result, key=lambda x: x['turnover_rate'], reverse=True))