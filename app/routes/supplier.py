from flask import Blueprint, render_template, request, jsonify
from app import db
from app.models import Supplier

bp = Blueprint('supplier', __name__)

@bp.route('/suppliers')
def suppliers():
    suppliers = Supplier.query.all()
    return render_template('supplier.html', suppliers=suppliers)

@bp.route('/supplier/add', methods=['POST'])
def add_supplier():
    try:
        data = request.json
        new_supplier = Supplier(
            name=data['name'],
            contact_person=data['contact_person'],
            phone=data['phone'],
            address=data['address']
        )
        db.session.add(new_supplier)
        db.session.commit()
        return jsonify({'success': True, 'message': '供应商添加成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'添加供应商失败: {str(e)}'}), 400

@bp.route('/supplier/<int:id>', methods=['GET'])
def get_supplier(id):
    supplier = Supplier.query.get_or_404(id)
    return jsonify({
        'supplier_id': supplier.supplier_id,
        'name': supplier.name,
        'contact_person': supplier.contact_person,
        'phone': supplier.phone,
        'address': supplier.address
    })

@bp.route('/supplier/edit/<int:id>', methods=['POST'])
def edit_supplier(id):
    try:
        data = request.json
        supplier = Supplier.query.get_or_404(id)
        supplier.name = data['name']
        supplier.contact_person = data['contact_person']
        supplier.phone = data['phone']
        supplier.address = data['address']

        db.session.commit()
        return jsonify({'success': True, 'message': '供应商修改成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'修改供应商失败: {str(e)}'}), 400

@bp.route('/supplier/delete/<int:id>', methods=['POST'])
def delete_supplier(id):
    try:
        supplier = Supplier.query.get_or_404(id)
        db.session.delete(supplier)
        db.session.commit()
        return jsonify({'success': True, 'message': '供应商删除成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'删除供应商失败: {str(e)}'}), 400

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