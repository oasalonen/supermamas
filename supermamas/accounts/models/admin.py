from supermamas.accounts.models.user import User
from supermamas.areas import District

class Admin(User):

    def __init__(self, init_dict = None):
        self["responsible_districts"] = []
        super().__init__(init_dict)

        if init_dict:
            responsible_districts = init_dict.get("responsible_districts")
            if responsible_districts:
                [self.add_responsible_district(District(district)) for district in responsible_districts]

        self.add_role(self.ROLE_ADMIN)

    @property
    def is_active(self):
        return True

    @property
    def responsible_districts(self):
        return self.get("responsible_districts")

    def add_responsible_district(self, district):
        district_ids = [d.id for d in self.responsible_districts]
        if district.id not in district_ids:
            self.responsible_districts.append(district)
            
