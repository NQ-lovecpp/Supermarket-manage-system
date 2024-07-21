from flask import Blueprint, render_template, request, jsonify
from app import db
from app.models import Purchase, Product, Supplier
from datetime import datetime

bp = Blueprint('purchase', __name__)

@bp.route('/purchases')
def purchases():
    purchases = Purchase.query.all()
    products = Product.query.all()
    suppliers = Supplier.query.all()
    return render_template('purchase.html', purchases=purchases, products=products, suppliers=suppliers)

@bp.route('/purchase/add', methods=['POST'])
def add_purchase():
    product_id = request.form['product_id']
    supplier_id = request.form['supplier_id']
    quantity = int(request.form['quantity'])
    unit_price = float(request.form['unit_price'])
    purchase_date = datetime.strptime(request.form['purchase_date'], '%Y-%m-%d').date()

    new_purchase = Purchase(product_id=product_id, supplier_id=supplier_id, quantity=quantity, unit_price=unit_price, purchase_date=purchase_date)
    db.session.add(new_purchase)

    # 更新库存
    product = Product.query.get(product_id)
    product.stock += quantity

    db.session.commit()

    return jsonify({'success': True})

@bp.route('/purchase/search')
def search_purchase():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    query = Purchase.query

    if start_date:
        query = query.filter(Purchase.purchase_date >= datetime.strptime(start_date, '%Y-%m-%d').date())
    if end_date:
        query = query.filter(Purchase.purchase_date <= datetime.strptime(end_date, '%Y-%m-%d').date())

    purchases = query.all()
    return jsonify([{
        'id': p.purchase_id,
        'product_name': p.product.name,
        'supplier_name': p.supplier.name,
        'quantity': p.quantity,
        'unit_price': float(p.unit_price),
        'purchase_date': p.purchase_date.strftime('%Y-%m-%d')
    } for p in purchases])