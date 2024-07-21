from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from app import db
from app.models import Supplier

bp = Blueprint('supplier', __name__)

@bp.route('/suppliers')
def suppliers():
    suppliers = Supplier.query.all()
    return render_template('supplier.html', suppliers=suppliers)

@bp.route('/supplier/add', methods=['POST'])
def add_supplier():
    name = request.form['name']
    contact_person = request.form['contact_person']
    phone = request.form['phone']
    address = request.form['address']

    new_supplier = Supplier(name=name, contact_person=contact_person, phone=phone, address=address)
    db.session.add(new_supplier)
    db.session.commit()

    return jsonify({'success': True})

@bp.route('/supplier/edit/<int:id>', methods=['POST'])
def edit_supplier(id):
    supplier = Supplier.query.get_or_404(id)
    supplier.name = request.form['name']
    supplier.contact_person = request.form['contact_person']
    supplier.phone = request.form['phone']
    supplier.address = request.form['address']

    db.session.commit()

    return jsonify({'success': True})

@bp.route('/supplier/delete/<int:id>', methods=['POST'])
def delete_supplier(id):
    supplier = Supplier.query.get_or_404(id)
    db.session.delete(supplier)
    db.session.commit()

    return jsonify({'success': True})

@bp.route('/supplier/search')
def search_supplier():
    query = request.args.get('query', '')
    suppliers = Supplier.query.filter(
        (Supplier.name.ilike(f'%{query}%')) |
        (Supplier.contact_person.ilike(f'%{query}%'))
    ).all()
    return jsonify([{
        'id': s.supplier_id,
        'name': s.name,
        'contact_person': s.contact_person,
        'phone': s.phone,
        'address': s.address
    } for s in suppliers])