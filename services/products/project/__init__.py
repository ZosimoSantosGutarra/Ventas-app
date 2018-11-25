# services/products/project/__init__.py


import os

from flask import Flask  # <-- nuevo
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
from flask_cors import CORS

# instanciado la db
db = SQLAlchemy()


# new
def create_app(script_info=None):
 
	# instantiate the app
	app = Flask(__name__)
 
	# enable CORS
	CORS(app)  # nuevo
 
	# set confige
	app_settings = os.getenv('APP_SETTINGS')
	app.config.from_object(app_settings)
 
	# set up extensions
	db.init_app(app)
	#toolbar.init_app(app)
 
	# register blueprints
	from project.api.products import products_blueprint 
	app.register_blueprint(products_blueprint)
 
	# shell context for flask cli
	@app.shell_context_processor
	def ctx():
            return {'app': app, 'db': db}
 
	return app
