# services/products/manage.py

import unittest
import coverage
from flask.cli import FlaskGroup

from project import create_app, db   # <-- nuevo
from project.api.models import Product  # <-- nuevo

# configurando informes de covertura con coverage 4.5.1
COV = coverage.coverage(
    branch=True,
    include='project/*',
    omit=[
        'project/tests/*',
        'project/config.py',
    ]
)
COV.start()

app = create_app()  # <-- nuevo
cli = FlaskGroup(create_app=create_app)  # <-- nuevo


@cli.command()
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command()
def test():
    """ Ejecuta las pruebas sin cobertura de codigo"""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

@cli.command()
def seed_db():
    """Seeds the database."""
    db.session.add(Product(nomb='Acido Muriatigo', cat="Limpieza", cod="123456789", stoc="20", prec="2000"))
    db.session.add(Product(nomb='Adaptador 36W', cat="Sect.Electrico", cod='20181109', stoc='10', prec='3000'))
    db.session.add(Product(nomb='Campeon 5g', cat="Limpieza", cod='3029405', stoc='12', prec='16'))
    db.session.add(Product(nomb=' BUSHING 1/2 ', cat="Conexiones", cod=' 101007', stoc='5', prec='25'))
    db.session.add(Product(nomb='Cabezal chino', cat="Limpieza", cod='30102020', stoc='50', prec='10'))
    db.session.add(Product(nomb='Cemento', cat="NAYLON Y OTROS", cod='12356789', stoc='100', prec='50'))
    db.session.commit()

@cli.command()
def cov():
    """Ejecuta las pruebas unitarias con covertura."""
    tests = unittest.TestLoader().discover('project/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Resumen de covertura:')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    return 1



if __name__ == '__main__':
    cli()

