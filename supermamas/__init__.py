import os

from flask import Flask, request, Response
from flask_pymongo import PyMongo

from supermamas import config
from supermamas import models

def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_object(config)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    mongo = PyMongo(app)

    @app.route("/hello")
    def hello():
        u = models.User()
        u.first_name = "abc"
        mongo.db.users.insert_one(u.__dict__)
        return 'Hello, World!'

    # apply the blueprints to the app
    from supermamas import root, auth
    app.register_blueprint(root.bp)
    app.register_blueprint(auth.bp)

    app.add_url_rule('/', endpoint='index')

    # Enable translation extension
    app.jinja_env.add_extension("jinja2.ext.i18n")
    app.jinja_env.install_null_translations()

    return app