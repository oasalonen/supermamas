from supermamas.areas import District, City

class Address(dict):
    def __init__(self, init_dict = None):
        if init_dict:
            self.update(init_dict)
            
            district = init_dict.get("district")
            if district:
                self.district = District(district)
            
            city = init_dict.get("city")
            if city:
                self.city = City(city)
        return

    @property
    def address_line1(self):
        return self.get("address_line1")

    @address_line1.setter
    def address_line1(self, value):
        self["address_line1"] = value

    @property
    def address_line2(self):
        return self.get("address_line2")

    @address_line2.setter
    def address_line2(self, value):
        self["address_line2"] = value

    @property
    def postal_code(self):
        return self.get("postal_code")

    @postal_code.setter
    def postal_code(self, value):
        self["postal_code"] = value

    @property
    def district(self):
        return self.get("district")

    @district.setter
    def district(self, value):
        self["district"] = value

    @property
    def city(self):
        return self.get("city")

    @city.setter
    def city(self, value):
        self["city"] = value