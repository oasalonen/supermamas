from supermamas.accounts.user import User

class Admin(User):

    def __init__(self, init_dict = None):
        super().__init__(init_dict)
        self.add_role(self.ROLE_ADMIN)

    @property
    def is_active(self):
        return True

    @property
    def responsible_districts(self):
        return self.get("responsible_districts", [])

    def add_responsible_district(self, district):
        districts = self.responsible_districts
        district_ids = [d.get("id") for d in districts]
        if district.id not in district_ids:
            districts.append({
                "id": district.id,
                "name": district.name
            })
            self["responsible_districts"] = districts
            
