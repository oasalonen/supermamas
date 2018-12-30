from wtforms.widgets import Input
from wtforms.ext.dateutil.fields import DateField

class CalendarField(DateField):
    widget = Input("date")