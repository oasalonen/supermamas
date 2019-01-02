from wtforms.widgets import Input
from wtforms.ext.dateutil.fields import DateField
from datetime import datetime

class CalendarField(DateField):
    widget = Input("date")

    def datetime(self):
        return datetime.combine(self.data, datetime.min.time())