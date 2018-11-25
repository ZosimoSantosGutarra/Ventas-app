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
    db.session.add(Product(nombre='Acido Muriatigo', categoria="Limpieza", codigo="123456789", stock="20", precio="2000"))
    db.session.add(Product(nombre='Adaptador 36W', categoria="Sect.Electrico", codigo='20181109', stock='10', precio='3000'))
    db.session.add(Product(nombre='Campeon 5g', categoria="Limpieza", codigo='3029405', stock='12', precio='16'))
    db.session.add(Product(nombre=' BUSHING 1/2 ', categoria="Conexiones", codigo=' 101007', stock='5', precio='25'))
    db.session.add(Product(nombre='Cabezal chino', categoria="Limpieza", codigo='30102020', stock='50', precio='10'))
    db.session.add(Product(nombre='Cemento', categoria="NAYLON Y OTROS", codigo='12356789', stock='100', precio='50'))
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
