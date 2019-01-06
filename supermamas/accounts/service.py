from supermamas.accounts import User

class AccountsService:
    __instance = None

    def __new__(cls, repository=None):
        if not AccountsService.__instance:
            AccountsService.__instance = object.__new__(cls)
            AccountsService.__instance.repository = repository
        return AccountsService.__instance

    def _repository(self):
        return self.__instance.repository

    def get_bubble_mamas(self):
        return self._repository().get_by_role(User.ROLE_BUBBLE_MAMA)

    def get_bubble_mama(self, bubble_mama_id):
        bubble_mama = self._repository().get(bubble_mama_id)
        if not bubble_mama:
            raise Exception("No such user", bubble_mama_id)
        if not bubble_mama.is_bubble_mama:
            raise Exception("User {} is not a bubble mama", bubble_mama_id)
        return bubble_mama