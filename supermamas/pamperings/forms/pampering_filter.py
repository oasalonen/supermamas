from wtforms import Form, SelectField
from flask_babel import gettext
from flask_login import current_user

class PamperingFilterForm(Form):
    created_by = SelectField(gettext(u""))
    district = SelectField(gettext(u"District"))
    status = SelectField(gettext(u"Status"), choices=["current", "all"])

    def is_filtered_by_current(self):
        return self.status.data == "current"