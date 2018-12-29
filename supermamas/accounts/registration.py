from flask_bcrypt import Bcrypt
from flask_babel import gettext
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from supermamas.common.template_renderer import TemplateRenderer
from supermamas.common.emailer import Emailer
from supermamas.accounts.user import User
from supermamas.accounts.admin import Admin
from supermamas import districts

class RegistrationService:
    __instance = None

    def __new__(cls, repository=None, app=None):
        if not RegistrationService.__instance:
            RegistrationService.__instance = object.__new__(cls)
            RegistrationService.__instance.repository = repository
            RegistrationService.__instance.bcrypt = Bcrypt(app)
            RegistrationService.__instance.app = app
        return RegistrationService.__instance

    def _repository(self):
        return self.__instance.repository

    def _bcrypt(self):
        return self.__instance.bcrypt

    def _app(self):
        return self.__instance.app

    def register(self, email, password, first_name, last_name, district_id):
        # Disallow multiple accounts with the same email
        if self._repository().get_by_email(email):
            return None

        district = districts.Service().get_district(district_id)
        if not district:
            raise Exception("District {} not found", district_id)

        password = self._bcrypt().generate_password_hash(password)
        user = User()
        user.email = email
        user.password = password
        user.first_name = first_name
        user.last_name = last_name
        user.district = district
        user.require_activation()

        user = self._repository().insert(user)
        self.send_activation_email(user)

        return user

    def register_admin(self, email, password, first_name, last_name, district_id, responsible_districts):
        # Disallow multiple accounts with the same email
        if self._repository().get_by_email(email):
            return None

        district = districts.Service().get_district(district_id)
        if not district:
            raise Exception("District {} not found", district_id)

        password = self._bcrypt().generate_password_hash(password)
        admin = Admin()
        admin.email = email
        admin.password = password
        admin.first_name = first_name
        admin.last_name = last_name
        admin.district = district

        responsible_districts = [districts.Service().get_district(id) for id in responsible_districts]
        for district in responsible_districts:
            admin.add_responsible_district(district)

        admin = self._repository().insert(admin)

        return admin

    def activate_user(self, user_id, code):
        user = self._repository().get(user_id)
        if not user:
            raise Exception("User not found")
        
        user.activate(code)
        self._repository().replace(user)

    def send_activation_email(self, user):
        message = MIMEMultipart("alternative")
        message["Subject"] = gettext(u"Activate your Supermamas account")
        message["From"] = Emailer().sender
        message["To"] = user.email

        activation_link = "{uri_base}/accounts/{id}/activation?code={code}".format(
            uri_base=self._app().config.get("URI_BASE"),
            id=user.id, 
            code=user.activation_code)

        # Simple fallback text message
        text = F"Go to the following link to activate your Supermamas account: {activation_link}"

        # HTML message
        html = TemplateRenderer().render(
            "activation_mail.html.j2", 
            name=user.first_name,
            activation_link=activation_link)

        message.attach(MIMEText(text, "plain"))
        message.attach(MIMEText(html, "html"))

        Emailer().send_message([user.email], message)
