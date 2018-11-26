# services/products/project/api/products.py

from flask import Blueprint, jsonify, request, render_template

from project.api.models import Product
from project import db

from sqlalchemy import exc


pro_blueprint = Blueprint('products', __name__, template_folder='./templates')


@pro_blueprint.route('/products/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'estado': 'satisfactorio',
        'mensaje': 'pong!!!'
    })


@pro_blueprint.route('/products', methods=['POST'])
def add_product():
    post_data = request.get_json()
    response_object = {
        'estado': 'fallo',
        'mensaje': 'Datos no validos.'
    }
    if not post_data:
        return jsonify(response_object), 400
    n = post_data.get('nomb')
    c = post_data.get('cat')
    cd = post_data.get('cod')
    s = post_data.get('stoc')
    p = post_data.get('prec')
    try:
        prod = Product.query.filter_by(nomb=n).first()
        if not prod:
            db.session.add(Product(nomb=n, cat=c, cod=cd, stoc=s, prec=p))
            db.session.commit()
            response_object['estado'] = 'satisfactorio'
            response_object['mensaje'] = f'{n}ha sido agregado al registro'
            return jsonify(response_object), 201
        else:
            response_object['mensaje'] = 'producto ya existe.'
            return jsonify(response_object), 400
    except exc.IntegrityError as e:
        db.session.rollback()
        return jsonify(response_object), 400


@pro_blueprint.route('/products/<product_id>', methods=['GET'])
def get_single_product(product_id):
    """Obteniendo detalles de un unico producto"""
    response_object = {
        'estado': 'fallo',
        'mensaje': 'Producto no existe'
    }

    try:
        prod = Product.query.filter_by(id=int(product_id)).first()
        if not prod:
            return jsonify(response_object), 404
        else:
            response_object = {
                'estado': 'satisfactorio',
                'data': {
                    'id': prod.id,
                    'nomb': prod.nomb,
                    'cat': prod.cat,
                    'cod': prod.cod,
                    'stoc': prod.stoc,
                    'prec': prod.prec
                }
            }
            return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404


@pro_blueprint.route('/products', methods=['GET'])
def get_all_products():
    """Get all products"""
    response_object = {
        'estado': 'satisfactorio',
        'data': {
            'products': [prod.to_json() for prod in Product.query.all()]
        }
    }
    return jsonify(response_object), 200


@pro_blueprint.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        n = request.form['nomb']
        c = request.form['cat']
        cd = request.form['cod']
        s = request.form['stoc']
        p = request.form['prec']
        db.session.add(Product(nomb=n, cat=c, cod=cd, stoc=s, prec=p))
        db.session.commit()
    products = Product.query.all()
    return render_template('index.html', products=products)
