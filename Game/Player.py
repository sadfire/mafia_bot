from Game.Roles import Roles
from Game.Cards import CardsBeginner as Cards


class Player:
    def __init__(self, member_id, name, role=Roles.Civilian, card=Cards.Neutral, is_alive=True) -> None:
        super().__init__()
        self.id = member_id
        self.name = name
        self.postfix = ""
        self.role = role
        self._card = card
        self.is_alive = is_alive
        self.number = None
