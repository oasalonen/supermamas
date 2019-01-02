from flask_bcrypt import Bcrypt
from flask_babel import gettext
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from supermamas.common.template_renderer import TemplateRenderer
from supermamas.common.emailer import Emailer
from supermamas.accounts import User, Admin, Address, BubbleMamaProfile
from supermamas.areas import AreaService

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

    def register_bubble_mama(self, form):
        # Disallow multiple accounts with the same email
        if self._repository().get_by_email(form.email.data):
            return None # Don't raise an exception to leak who is registered

        city = AreaService().get_city(form.city.data)
        if not city:
            raise Exception("City {} not found", form.city.data)

        district = AreaService().get_district(form.district.data)
        if not district:
            raise Exception("District {} not found", form.district.data)

        user = User()
        user.email = form.email.data
        user.password = self._bcrypt().generate_password_hash(form.password.data)
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data

        address = Address()
        address.address_line1 = form.address_line1.data
        address.address_line2 = form.address_line2.data
        address.postal_code = form.postal_code.data
        address.city = city
        address.district = district
        user.address = address

        profile = BubbleMamaProfile()
        profile.pampering_type = form.pampering_type.data
        profile.due_date = form.due_date.datetime()
        profile.pampering_start_date = form.pampering_start_date.datetime()
        profile.baby_name = form.baby_name.data
        profile.baby_birth_date = form.baby_birth_date.datetime()
        profile.preferred_pampering_days = form.pampering_days.options.data
        profile.max_pamperings_per_week = form.max_pamperings_per_week.data
        profile.family_situation = form.family_situation.data
        profile.food_allergies = form.food_allergies.data
        profile.diet_restrictions = form.diet_restrictions.data
        profile.languages = form.get_languages()
        profile.personal_message = form.personal_message.data
        profile.referrer = form.referrer.data
        profile.accept_contact_detail_sharing = form.accept_contact_detail_sharing.data
        profile.accept_welcome_helping_mamas = form.accept_welcome_helping_mamas.data
        profile.accept_notify_helping_mamas = form.accept_notify_helping_mamas.data
        profile.accept_thank_helping_mamas = form.accept_thank_helping_mamas.data
        profile.accept_diversity = form.accept_diversity.data
        profile.allow_helping_dads = form.allow_helping_dads.data
        user.bubble_mama_profile = profile

        user.add_role(user.ROLE_BUBBLE_MAMA)

        user.require_activation()

        user = self._repository().insert(user)
        self.send_activation_email(user)

        return user

    def register_admin(self, email, password, first_name, last_name, district_id, responsible_districts):
        # Disallow multiple accounts with the same email
        if self._repository().get_by_email(email):
            return None

        district = AreaService().get_district(district_id)
        if not district:
            raise Exception("District {} not found", district_id)

        password = self._bcrypt().generate_password_hash(password)
        admin = Admin()
        admin.email = email
        admin.password = password
        admin.first_name = first_name
        admin.last_name = last_name
        admin.district = district

        responsible_districts = [AreaService().get_district(id) for id in responsible_districts]
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
