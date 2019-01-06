from supermamas.common.configuration_service import ConfigurationService
from supermamas.common.template_renderer import TemplateRenderer
from supermamas.common.emailer import Emailer
from supermamas.common import router_utils
from supermamas.common.datetime import weekdays

def init(app):
    ConfigurationService(app.config)
    TemplateRenderer(app.jinja_env)
    Emailer(app)