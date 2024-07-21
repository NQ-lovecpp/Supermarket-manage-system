from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from app import db
from app.models import Product, Category, Supplier

bp = Blueprint('product', __name__)

@bp.route('/products')
def products():
    products = Product.query.all()
    categories = Category.query.all()
    suppliers = Supplier.query.all()
    return render_template('product.html', products=products, categories=categories, suppliers=suppliers)

@bp.route('/product/add', methods=['POST'])
def add_product():
    name = request.form['name']
    category_id = request.form['category_id']
    price = request.form['price']
    stock = request.form['stock']
    supplier_id = request.form['supplier_id']

    new_product = Product(name=name, category_id=category_id, price=price, stock=stock, supplier_id=supplier_id)
    db.session.add(new_product)
    db.session.commit()

    return redirect(url_for('product.products'))

@bp.route('/product/edit/<int:id>', methods=['POST'])
def edit_product(id):
    product = Product.query.get_or_404(id)
    product.name = request.form['name']
    product.category_id = request.form['category_id']
    product.price = request.form['price']
    product.stock = request.form['stock']
    product.supplier_id = request.form['supplier_id']

    db.session.commit()

    return redirect(url_for('product.products'))

@bp.route('/product/delete/<int:id>', methods=['POST'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()

    return redirect(url_for('product.products'))

@bp.route('/product/search')
def search_product():
    query = request.args.get('query', '')
    products = Product.query.filter(Product.name.ilike(f'%{query}%')).all()
    return jsonify([{'id': p.product_id, 'name': p.name, 'category': p.category.name, 'price': float(p.price), 'stock': p.stock, 'supplier': p.supplier.name} for p in products])