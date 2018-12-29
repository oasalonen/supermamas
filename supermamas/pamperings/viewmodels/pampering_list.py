from flask import url_for

class PamperingListViewModel(dict):

    def set_pamperings(self, pamperings):
        self["pamperings"] = [self.create_list_item(pampering) for pampering in pamperings]

    def create_list_item(self, pampering):
        return {
            "id": pampering.id,
            "bubble_mama": pampering.bubble_mama["first_name"] + " " + pampering.bubble_mama["last_name"],
            "district": pampering.district["name"],
            "start_date": pampering.start_date.date(),
            "end_date": pampering.end_date.date(),
            "detail_link": url_for("pamperings.get_details", id=pampering.id)
        }