import requests
from flask import request
from flask_babel import gettext
from wtforms import HiddenField

from supermamas.common.configuration_service import ConfigurationService

class RecaptchaField(HiddenField):
    def process(self, formdata):
        self.data = formdata.get("g-recaptcha-response")

    def validate(self, form, extra_validators=tuple()):
        result = requests.post("https://www.google.com/recaptcha/api/siteverify", data={
            "secret": ConfigurationService().get("RECAPTCHA_SECRET"), 
            "response": self.data, 
            "remoteip": request.remote_addr
            })
        if result and result.status_code == 200:
            if result.json() and result.json().get("success"):
                return True
        self.errors = [gettext(u"Recaptcha check failed")]
        return False