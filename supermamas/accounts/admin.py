from supermamas.accounts.user import User

class Admin(User):

    @property
    def is_active(self):
        return True

    @property
    def is_admin(self):
        return True

    @property
    def responsible_districts(self):
        return self.get("responsible_districts", [])

    @property
    def add_responsible_district(self, district):
        district_ids = [d.get("id") for d in self.responsible_districts]
        if district.id not in district_ids:
            self.responsible_districts.append({
                "id": district.id,
                "name": district.name
            })
