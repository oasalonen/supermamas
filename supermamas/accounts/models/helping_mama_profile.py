from supermamas.common import Model

class HelpingMamaProfile(Model):

    @property
    def good_to_know(self):
        return self.get("good_to_know")

    @good_to_know.setter
    def good_to_know(self, value):
        self["good_to_know"] = value

    @property
    def speciality(self):
        return self.get("speciality")

    @speciality.setter
    def speciality(self, value):
        self["speciality"] = value

    @property
    def personal_experience(self):
        return self.get("personal_experience")

    @personal_experience.setter
    def personal_experience(self, value):
        self["personal_experience"] = value

    @property
    def personal_message(self):
        return self.get("personal_message")

    @personal_message.setter
    def personal_message(self, value):
        self["personal_message"] = value

    @property
    def accept_contact_detail_sharing(self):
        return self.get("accept_contact_detail_sharing")

    @accept_contact_detail_sharing.setter
    def accept_contact_detail_sharing(self, value):
        self["accept_contact_detail_sharing"] = value

    @property
    def accept_diversity(self):
        return self.get("accept_diversity")

    @accept_diversity.setter
    def accept_diversity(self, value):
        self["accept_diversity"] = value