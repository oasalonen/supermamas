from wtforms import SelectMultipleField
from wtforms.widgets import ListWidget, CheckboxInput, html_params, HTMLString
from dateutil import parser

class CalendarWidget(ListWidget):
    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        html = ['<%s %s>' % (self.html_tag, html_params(**kwargs))]

        is_first_subfield = True
        for subfield in field:
            if is_first_subfield:
                is_first_subfield = False
                for _ in range(parser.parse(subfield.data).date().weekday() - 0):
                    html.append('<li class="cell empty"></li>')

            if self.prefix_label:
                html.append('<li class="cell"><div class="container">%s %s</div></li>' % (subfield.label, subfield()))
            else:
                html.append('<li class="cell"><div class="container">%s %s</div></li>' % (subfield(), subfield.label))
        html.append('</%s>' % self.html_tag)
        return HTMLString(''.join(html))

class CalendarSelectField(SelectMultipleField):
    widget = CalendarWidget(prefix_label=False)
    option_widget = CheckboxInput()

    def get_datetimes(self):
        return [parser.parse(isodate) for isodate in self.data]
