import os

from flask import Flask, request, Response
from flask_babel import Babel
from sassutils.wsgi import SassMiddleware

from supermamas import config
from supermamas import accounts
from supermamas import pamperings

def debug(text):
  print(text)
  return ''

def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.secret_key = config.APP_SECRET
    app.jinja_env.filters['debug']=debug

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
    
    # Enable per-request-Sass
    # To enable it per-deployment, see https://sass.github.io/libsass-python/frameworks/flask.html#id6
    app.wsgi_app = SassMiddleware(app.wsgi_app, {
        'supermamas': ('static/sass', 'static/css', '/static/css')
    })
    import logging
    logging.basicConfig()

    accounts.init(app)
    pamperings.init(app)

    # apply the blueprints to the app
    from supermamas import root, auth, pampering
    app.register_blueprint(root.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(pampering.bp)

    app.add_url_rule('/', endpoint='index')

    # Enable translation extension
    app.jinja_env.add_extension("jinja2.ext.i18n")
    app.jinja_env.install_null_translations()
    babel = Babel(app)

    return app