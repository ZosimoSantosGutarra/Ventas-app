# services/products/project/api/products.py

from flask import Blueprint, jsonify, request, render_template

from project.api.models import Product
from project import db

from sqlalchemy import exc


products_blueprint = Blueprint('products', __name__, template_folder='./templates')


@products_blueprint.route('/products/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'estado': 'satisfactorio',
        'mensaje': 'pong!!!'
    })


@products_blueprint.route('/products', methods=['POST'])
def add_product():
    post_data = request.get_json()
    response_object = {
        'estado': 'fallo',
        'mensaje': 'Datos no validos.'
    }
    if not post_data:
        return jsonify(response_object), 400
    nombre = post_data.get('nombre')
    categoria = post_data.get('categoria')
    codigo = post_data.get('codigo')
    stock = post_data.get('stock')
    precio = post_data.get('precio')
    try:
        prod = Product.query.filter_by(nombre=nombre).first()
        if not prod:
            db.session.add(Product(nombre=nombre, categoria=categoria, codigo=codigo,
                                   stock=stock, precio=precio))
            db.session.commit()
            response_object['estado'] = 'satisfactorio'
            response_object['mensaje'] = f'{nombre}ha sido agregado al registro'
            return jsonify(response_object), 201
        else:
            response_object['mensaje'] = 'Este nombre del producto ya existe en el registro.'
            return jsonify(response_object), 400
    except exc.IntegrityError as e:
        db.session.rollback()
        return jsonify(response_object), 400


@products_blueprint.route('/products/<product_id>', methods=['GET'])
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
                    'nombre': prod.nombre,
                    'categoria': prod.categoria,
                    'codigo': prod.codigo,
                    'stock': prod.stock,
                    'precio': prod.precio
                }
            }
            return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404



@products_blueprint.route('/products', methods=['GET'])
def get_all_products():
    """Get all products"""
    response_object = {
        'estado': 'satisfactorio',
        'data': {
            'products': [prod.to_json() for prod in Product.query.all()]
        }
    }
    return jsonify(response_object), 200


@products_blueprint.route('/products/<product_id>', methods=['PUT', 'DELETE'])
def single_product(product_id):
    response_object = {
      'status': 'success',
      'container_id': os.uname()[1]
    }
    produ = Product.query.filter_by(id=product_id).first()
    if request.method == 'PUT':
        post_data = request.get_json()
        produ.nombre = post_data.get('nombre')
        produ.categoria = post_data.get('categoria')
        produ.codigo = post_data.get('codigo')
        produ.stock = post_data.get('stock')
        produ.precio = post_data.get('precio')
        db.session.commit()
        response_object['message'] = 'Producto actualizado!'
    if request.method == 'DELETE':
        db.session.delete(produ)
        db.session.commit()
        response_object['message'] = 'Producto Eliminado!'
    return jsonify(response_object)



@products_blueprint.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nombre = request.form['nombre']
        categoria = request.form['categoria']
        codigo = request.form['codigo']
        stock = request.form['stock']
        precio = request.form['precio']
        db.session.add(Product(nombre=nombre, categoria=categoria, codigo=codigo, 
            stock=stock, precio=precio))
        db.session.commit()
    products = Product.query.all()
    return render_template('index.html', products=products)
