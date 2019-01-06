from flask import url_for
from flask_babel import gettext

from supermamas.accounts import AccountsService
from supermamas.pamperings import PamperingService

class BubbleMamaListViewModel(dict):

    def __init__(self):
        self._accounts_service = AccountsService()
        self._pampering_service = PamperingService()

        self.set_bubble_mamas(self._accounts_service.get_bubble_mamas())

    def set_bubble_mamas(self, bubble_mamas):
        bubble_mama_ids = [bubble_mama.id for bubble_mama in bubble_mamas]
        pamperings = self._pampering_service.get_by_bubble_mamas(bubble_mama_ids)
        self["bubble_mamas"] = [self.create_list_item(bubble_mama, pamperings.get(bubble_mama.id)) for bubble_mama in bubble_mamas]

    def create_list_item(self, bubble_mama, pampering):
        try:
            district = bubble_mama.address.district.name
        except:
            district = None

        return {
            "id": bubble_mama.id,
            "name": bubble_mama.full_name,
            "district": district,
            "pampering": self.create_pampering_cell(bubble_mama, pampering)
        }

    def create_pampering_cell(self, bubble_mama, pampering):
        return {
            "label": gettext(u"View") if pampering else gettext(u"Create"),
            "link": self.create_pampering_link(bubble_mama, pampering)
        }

    def create_pampering_link(self, bubble_mama, pampering):
        if pampering:
            return url_for("pamperings.get_details", id=pampering.id)
        else:
            return url_for("pamperings.create", bubble_mama=bubble_mama.id)