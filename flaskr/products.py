from flask import (
  Blueprint, request
)

from flaskr.db import get_db
import json

bp = Blueprint('products', __name__)

@bp.route('/products', methods=('GET', 'POST'))
def products():
  if request.method == 'GET':
    prod_id = request.args.get('prod_id')
    if not prod_id:
      return {'status': 'error', 'message': 'missing prod_id param'}
    
    db = get_db()
    product = db.execute(
      'SELECT * FROM products WHERE id = ?', (prod_id,)
    ).fetchone()
    
    if product is None:
      return {'status': 'error', 'message': 'product not found'}
    
    return {
      'status': 'success',
      'product': dict(zip(['id', 'name', 'price', 'quantity'], tuple(product)))
    }
    
    
  if request.method == 'POST':
    name = request.form['name']
    price = request.form['price']
    quantity = request.form['quantity']
    
    db = get_db()
    error = None
    
    if not name:
      error = 'name is required'
    elif not price:
      error = 'price is required'
    elif not quantity:
      error = 'price is required'
    
    if error is None:
      try:
        db.execute(
          'INSERT INTO products (name, price, quantity) VALUES (?, ?, ?)',
          (name, price, quantity)
        )
        db.commit()
      except:
        return {'status': 'error', 'message': 'an error happened and your product wasn\'t added'}
      else:
        return {'status': 'success', 'message': 'Your product as added successfully'}
    