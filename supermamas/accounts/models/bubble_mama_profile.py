from supermamas.common import Model

class BubbleMamaProfile(Model):

    @property
    def pampering_type(self):
        return self.get("pampering_type")

    @pampering_type.setter
    def pampering_type(self, value):
        self["pampering_type"] = value

    @property
    def due_date(self):
        return self.get("due_date")

    @due_date.setter
    def due_date(self, value):
        self["due_date"] = value

    @property
    def pampering_start_date(self):
        return self.get("pampering_start_date")

    @pampering_start_date.setter
    def pampering_start_date(self, value):
        self["pampering_start_date"] = value

    @property
    def baby_name(self):
        return self.get("baby_name")

    @baby_name.setter
    def baby_name(self, value):
        self["baby_name"] = value

    @property
    def baby_birth_date(self):
        return self.get("baby_birth_date")

    @baby_birth_date.setter
    def baby_birth_date(self, value):
        self["baby_birth_date"] = value

    @property
    def preferred_pampering_days(self):
        return self.get("preferred_pampering_days")

    @preferred_pampering_days.setter
    def preferred_pampering_days(self, value):
        self["preferred_pampering_days"] = value

    @property
    def max_pamperings_per_week(self):
        return self.get("max_pamperings_per_week")

    @max_pamperings_per_week.setter
    def max_pamperings_per_week(self, value):
        self["max_pamperings_per_week"] = value

    @property
    def family_situation(self):
        return self.get("family_situation")

    @family_situation.setter
    def family_situation(self, value):
        self["family_situation"] = value

    @property
    def food_allergies(self):
        return self.get("food_allergies")

    @food_allergies.setter
    def food_allergies(self, value):
        self["food_allergies"] = value

    @property
    def diet_restrictions(self):
        return self.get("diet_restrictions")

    @diet_restrictions.setter
    def diet_restrictions(self, value):
        self["diet_restrictions"] = value

    @property
    def languages(self):
        return self.get("languages")

    @languages.setter
    def languages(self, value):
        self["languages"] = value

    @property
    def personal_message(self):
        return self.get("personal_message")

    @personal_message.setter
    def personal_message(self, value):
        self["personal_message"] = value

    @property
    def accept_contact_detail_sharing(self):
        return self.get("accept_contact_detail_sharing", False)

    @accept_contact_detail_sharing.setter
    def accept_contact_detail_sharing(self, value):
        self["accept_contact_detail_sharing"] = value

    @property
    def accept_welcome_helping_mamas(self):
        return self.get("accept_welcome_helping_mamas", False)

    @accept_welcome_helping_mamas.setter
    def accept_welcome_helping_mamas(self, value):
        self["accept_welcome_helping_mamas"] = value

    @property
    def accept_notify_helping_mamas(self):
        return self.get("accept_notify_helping_mamas", False)

    @accept_notify_helping_mamas.setter
    def accept_notify_helping_mamas(self, value):
        self["accept_notify_helping_mamas"] = value

    @property
    def accept_thank_helping_mamas(self):
        return self.get("accept_thank_helping_mamas", False)

    @accept_thank_helping_mamas.setter
    def accept_thank_helping_mamas(self, value):
        self["accept_thank_helping_mamas"] = value

    @property
    def accept_diversity(self):
        return self.get("accept_diversity", False)

    @accept_diversity.setter
    def accept_diversity(self, value):
        self["accept_diversity"] = value

    @property
    def allow_helping_dads(self):
        return self.get("allow_helping_dads", False)

    @allow_helping_dads.setter
    def allow_helping_dads(self, value):
        self["allow_helping_dads"] = value

    