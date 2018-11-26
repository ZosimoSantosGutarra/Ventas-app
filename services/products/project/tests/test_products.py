# services/products/project/tests/test_products.py

from project import db
from project.api.models import Product

import json
import unittest

from project.tests.base import BaseTestCase


def add_product(nomb, cat, cod, stoc, prec):
    prod = Product(nomb=nomb, cat=cat, cod=cod, stoc=stoc, prec=prec)
    db.session.add(prod)
    db.session.commit()
    return prod


class TestProductService(BaseTestCase):
    """Prueba para el servicio products."""

    def test_products(self):
        """Asegurando que la ruta /ping se comporta correctamente."""
        response = self.client.get('/products/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!!!', data['mensaje'])
        self.assertIn('satisfactorio', data['estado'])

    def test_add_product(self):
        """Asegurando de que se pueda agregar un nuevo Producto a la base de
        datos."""
        with self.client:
            response = self.client.post(
                '/products',
                data=json.dumps({
                    'nomb': 'Adaptador universal ',
                    'cat': 'Sect.Electrico',
                    'cod': '10002000',
                    'stoc': '50',
                    'prec': '10'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('satisfactorio', data['estado'])

    def test_add_product_invalid_json(self):
        """Asegurando de que se arroje un error si el objeto json esta
        vacio."""
        with self.client:
            response = self.client.post(
                '/products',
                data=json.dumps({}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Datos no validos.', data['mensaje'])
            self.assertIn('fallo', data['estado'])

    def test_add_product_invalid_json_keys(self):
        """
        Asegurando de que se produce un error si el objeto JSON no tiene
        un key de nombre del producto.
        """
        with self.client:
            response = self.client.post(
                '/products',
                data=json.dumps({'nomb': 'Adaptador universal'}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Datos no validos.', data['mensaje'])
            self.assertIn('fallo', data['estado'])

    def test_add_product_duplicate_nombre(self):
        """Asegurando de que se produce un error si el nombre del producto ya
        existe."""
        with self.client:
            self.client.post(
                '/products',
                data=json.dumps({
                    'nomb': 'Adaptador universal',
                    'cat': 'Artefacto'
                }),
                content_type='application/json',
            )
            response = self.client.post(
                '/products',
                data=json.dumps({
                    'nomb': 'Adaptador universal',
                    'cat': 'Sect.Electrico'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('fallo', data['estado'])

    def test_single_product(self):
        """Asegurando de que el producto individual se comporte
        correctamente."""
        user = add_product('Adaptador universal', 'Sect.Electrico', '10002000', '50', '10')
        with self.client:
            response = self.client.get(f'/products/{user.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('Adaptador universal', data['data']['nomb'])
            self.assertIn('Sect.Electrico', data['data']['cat'])
            self.assertIn('10002000', data['data']['cod'])
            self.assertIn('50', data['data']['stoc'])
            self.assertIn('10', data['data']['prec'])
            self.assertIn('satisfactorio', data['estado'])

    def test_single_product_no_id(self):
        """Asegurando de que se lanze un error si no se proporciona un id."""
        with self.client:
            response = self.client.get('/products/blah')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('Producto no existe', data['mensaje'])
            self.assertIn('fallo', data['estado'])

    def test_single_product_incorrect_id(self):
        """Asegurando de que se lanze un error si el id no existe."""
        with self.client:
            response = self.client.get('/products/999')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('Producto no existe', data['mensaje'])
            self.assertIn('fallo', data['estado'])

    def test_all_products(self):
        """Asegurarse de que todos los productos se comporte correctamente."""
        add_product('Adaptador universal', 'Sect.Electrico', '10002000', '50', '10')
        add_product('Acido Muriatigo', 'Limpieza', '10102834', '10', '30')
        with self.client:
            response = self.client.get('/products')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['products']), 2)
            self.assertIn('Adaptador universal', data['data']['products'][0]['nomb'])
            self.assertIn(
                'Sect.Electrico', data['data']['products'][0]['cat'])
            self.assertIn('Acido Muriatigo', data['data']['products'][1]['nomb'])
            self.assertIn(
                'Limpieza', data['data']['products'][1]['cat'])
            self.assertIn('satisfactorio', data['estado'])

    def test_main_no_products(self):
        """."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_main_with_products(self):
        """Ensure the main route behaves correctly when users have been
        added to the database."""
        add_product('Adaptador universal', 'Sect.Electrico', '10002000', '50', '10')
        add_product('Acido Muriatigo', 'Limpieza', '10102834', '10', '30')
        with self.client:
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)

    def test_main_add_product(self):
        """Ensure a new user can be added to the database."""
        with self.client:
            response = self.client.post(
                '/',
                data=dict(nomb='Adaptador universal', cat='Sect.Electrico', cod='10002000', stoc='50', prec='10'),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
