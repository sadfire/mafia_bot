from GameLogic import GameInfo as GI, Event, Cards, Roles
from GameLogic.Models import ICardModel


class ListenerModel(ICardModel):
    def __init__(self, game) -> None:
        super().__init__(game)
        self._event = Event.SuccessListen, Event.FailedListen

    @property
    def get_result(self):
        if self.game[self._initiator][GI.Role] is Roles.Civilian:
            return self.game[self._target][GI.Role] is Roles.Mafia

        if self.game[self._initiator][GI.Role] is Roles.Mafia:
            return self.game[self._initiator][GI.Role] is Roles.Commissar

        else:
            raise ValueError("Commissar can't use Listener card")

    @property
    def next_state(self):
        from GameLogic.Models.Cards import HealModel
        from GameView import CardView

        return CardView, HealModel

    @property
    def get_card(self):
        return Cards.Listener

    def get_candidate(self, is_target):
        if is_target:
            return [number for number in self.game.get_alive() if number != self._initiator]

        return [number for number in self.game.get_alive(Roles.Commissar, is_card_closed=True, is_role_reverse=True)]
    @property
    def is_target_needed(self):
        return True

    def end(self):
        if super().end():
            return "Игрок услышал {}" + self.game[self._target].get_role_str

        return None
