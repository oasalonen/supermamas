from wtforms import (
    Field, 
    FormField, 
    StringField, 
    RadioField, 
    Form, 
    FormField, 
    BooleanField, 
    SelectMultipleField,
    ValidationError)
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

class OtherField(StringField):
    parent = None

    def __call__(self, **kwargs):
        group = self.parent.options.id
        sanitized_group = group.replace("-", "_")
        other_id = self.id
        other = "Other"
        script = '''
        <script>
        var check_other_%s = function() {
            var checkedRadio = document.querySelector('input[name="%s"]:checked');
            var otherInput = document.getElementById("%s");
            otherInput.disabled = !checkedRadio || checkedRadio.value !== "%s";
        };

        check_other_%s();

        document.getElementsByName("%s").forEach(function (radio) {
            radio.addEventListener("change", check_other_%s);
        });
        </script>
        ''' % (sanitized_group, group, other_id, other, sanitized_group, group, sanitized_group)

        return super().__call__(**kwargs) + script

class RadioWithOtherForm(Form):
    options = RadioField("")
    other = OtherField(gettext(u"Other"))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.other.parent = self

    def set_required(self, required):
        self.options.flags.required = True

    def validate_other(self, field):
        if self.options.flags.required:
            if (not self.options.data) or (self.options.data == "Other" and not self.other.data):
                raise ValidationError(gettext(u"Please select an option or fill in the \"Other\" field"))

class SelectWithOtherForm(Form):
    options = SelectMultipleField("")
    other = StringField(gettext(u"Other"))