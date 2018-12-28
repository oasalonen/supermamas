
class TemplateRenderer:
    __instance = None

    def __new__(cls, jinja_env=None):
        if not TemplateRenderer.__instance:
            TemplateRenderer.__instance = object.__new__(cls)
            TemplateRenderer.__instance.jinja_env = jinja_env
        return TemplateRenderer.__instance

    def _jinja_env(self):
        return self.__instance.jinja_env

    def render(self, template, *args, **kwargs):
        html = self._jinja_env().get_template(template)
        return html.render(*args, **kwargs)