from wtforms import Field, FormField, StringField, RadioField, Form, FormField, BooleanField, SelectMultipleField
from wtforms.widgets import html_params, HTMLString
from flask_babel import gettext

class DivWidget(object):
    def __init__(self, html_tag='div', prefix_label=True):
        self.html_tag = html_tag
        self.prefix_label = prefix_label

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        html = ['<%s %s>' % (self.html_tag, html_params(**kwargs))]
        for subfield in field:
            if self.prefix_label:
                html.append('<%s>%s %s</%s>' % (self.html_tag, subfield.label, subfield(), self.html_tag))
            else:
                html.append('<%s>%s %s</%s>' % (self.html_tag, subfield(), subfield.label, self.html_tag))
        html.append('</%s>' % self.html_tag)
        return HTMLString(''.join(html))


class ListFormField(FormField):
    widget = DivWidget()

class RadioWithOtherForm(Form):
    options = RadioField("")
    other = StringField(gettext(u"Other"))

class SelectWithOtherForm(Form):
    options = SelectMultipleField("")
    other = StringField(gettext(u"Other"))