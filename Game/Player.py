class Player:
    def __init__(self, member_id, role, card) -> None:
        super().__init__()
        self._id = member_id
        self._role = role
        self._card = card