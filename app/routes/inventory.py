from flask import Blueprint, render_template, request, jsonify
from app import db
from app.models import Product, Category

bp = Blueprint('inventory', __name__)

@bp.route('/inventory')
def inventory():
    products = Product.query.all()
    categories = Category.query.all()
    return render_template('inventory.html', products=products, categories=categories)

@bp.route('/inventory/set_alert', methods=['POST'])
def set_alert():
    product_id = request.form['product_id']
    alert_threshold = int(request.form['alert_threshold'])

    product = Product.query.get_or_404(product_id)
    product.alert_threshold = alert_threshold
    db.session.commit()

    return jsonify({'success': True})

@bp.route('/inventory/filter')
def filter_inventory():
    category_id = request.args.get('category_id')
    min_stock = request.args.get('min_stock')
    max_stock = request.args.get('max_stock')

    query = Product.query

    if category_id:
        query = query.filter(Product.category_id == category_id)
    if min_stock:
        query = query.filter(Product.stock >= int(min_stock))
    if max_stock:
        query = query.filter(Product.stock <= int(max_stock))

    products = query.all()
    return jsonify([{
        'id': p.product_id,
        'name': p.name,
        'category': p.category.name,
        'stock': p.stock,
        'alert_threshold': p.alert_threshold or 0
    } for p in products])

@bp.route('/inventory/report')
def generate_report():
    products = Product.query.all()
    report = []
    for product in products:
        report.append({
            'id': product.product_id,
            'name': product.name,
            'category': product.category.name,
            'current_stock': product.stock,
            'alert_threshold': product.alert_threshold or 0,
            'status': 'Low' if product.stock < (product.alert_threshold or 0) else 'Normal'
        })
    return jsonify(report)