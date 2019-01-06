from flask import url_for

from supermamas.accounts import AccountsService

class CreatePamperingViewModel(dict):

    def __init__(self, bubble_mama_id):
        bubble_mama = AccountsService().get_bubble_mama(bubble_mama_id)
        self.set_bubble_mama(bubble_mama)

    def set_bubble_mama(self, bubble_mama):
        self["bubble_mama"] = {
            "name": bubble_mama.full_name,
            "profile": bubble_mama.bubble_mama_profile
        }
